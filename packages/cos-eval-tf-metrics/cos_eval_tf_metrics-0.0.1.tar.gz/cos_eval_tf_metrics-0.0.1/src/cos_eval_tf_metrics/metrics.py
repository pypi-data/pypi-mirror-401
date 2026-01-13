import tensorflow as tf

# ==========================================
# 1. S-Score Metric
# ==========================================
class SScore(tf.keras.metrics.Metric):
    def __init__(self, alpha=0.5, name="s_score", **kwargs):
        super(SScore, self).__init__(name=name, **kwargs)
        self.alpha = alpha  # Weight for S_o (Object Similarity)
        self.s_object = self.add_weight(name="so", initializer="zeros")
        self.s_region = self.add_weight(name="sr", initializer="zeros")
        self.count = self.add_weight(name="count", initializer="zeros")

    def f_score(self, y_true, y_pred, smooth=1.0):
        """Compute the F1-score (Dice Similarity)"""
        y_pred = tf.cast(y_pred > 0.5, tf.float32)
        y_true = tf.cast(y_true, tf.float32)

        intersection = tf.reduce_sum(y_true * y_pred)
        tp_fp = tf.reduce_sum(y_pred)
        tp_fn = tf.reduce_sum(y_true)

        f1 = (2.0 * intersection + smooth) / (tp_fp + tp_fn + smooth)
        return f1

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_pred = tf.clip_by_value(y_pred, 0.0, 1.0)
        so = self.f_score(y_true, y_pred)
        sr = tf.reduce_mean(tf.image.ssim(y_true, y_pred, max_val=1.0))

        self.s_object.assign_add(so)
        self.s_region.assign_add(sr)
        self.count.assign_add(1.0)

    def result(self):
        return (self.alpha * self.s_object + (1 - self.alpha) * self.s_region) / (self.count + tf.keras.backend.epsilon())

    def reset_state(self):
        self.s_object.assign(0.0)
        self.s_region.assign(0.0)
        self.count.assign(0.0)


# ==========================================
# 2. E-Similarity Metric
# ==========================================
def e_similarity(pred, mask, threshold=0.5):
    pred_binary = tf.where(pred > threshold, 1.0, 0.0)
    
    mpred = tf.reduce_mean(pred_binary, axis=[2, 3], keepdims=True)
    phiFM = pred_binary - mpred
    
    mmask = tf.reduce_mean(mask, axis=[2, 3], keepdims=True)
    phiGT = mask - mmask
    
    EFM = (2.0 * phiFM * phiGT + 1e-8) / (phiFM * phiFM + phiGT * phiGT + 1e-8)
    QFM = (1 + EFM) * (1 + EFM) / 4.0
    similarity = tf.reduce_mean(QFM, axis=[2, 3])
    
    return tf.reduce_mean(similarity)

class ESimilarityMetric(tf.keras.metrics.Metric):
    def __init__(self, name='e_similarity', **kwargs):
        super(ESimilarityMetric, self).__init__(name=name, **kwargs)
        self.total_similarity = self.add_weight(name='total', initializer='zeros')
        self.count = self.add_weight(name='count', initializer='zeros')

    def update_state(self, y_true, y_pred, sample_weight=None):
        similarity = e_similarity(y_pred, y_true)
        self.total_similarity.assign_add(similarity)
        self.count.assign_add(1.0)

    def result(self):
        return self.total_similarity / self.count

    def reset_state(self):
        self.total_similarity.assign(0.0)
        self.count.assign(0.0)


# ==========================================
# 3. Weighted F-Score Metric
# ==========================================
def weighted_f_score(y_true, y_pred, beta=0.3, threshold=0.5):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred >= threshold, tf.float32)

    tp = tf.reduce_sum(y_true * y_pred)
    fp = tf.reduce_sum((1 - y_true) * y_pred)
    fn = tf.reduce_sum(y_true * (1 - y_pred))

    precision = tp / (tp + fp + 1e-7)
    recall = tp / (tp + fn + 1e-7)

    beta_sq = beta
    f_score = (1 + beta_sq) * (precision * recall) / (beta_sq * precision + recall + 1e-7)

    return f_score

class WeightedFScoreMetric(tf.keras.metrics.Metric):
    def __init__(self, beta=0.3, name="weighted_f_score", **kwargs):
        super(WeightedFScoreMetric, self).__init__(name=name, **kwargs)
        self.beta = beta
        self.scores = self.add_weight(name="f_scores", initializer="zeros")
        self.count = self.add_weight(name="count", initializer="zeros")

    def update_state(self, y_true, y_pred, sample_weight=None):
        best_fbeta = weighted_f_score(y_true, y_pred, beta=self.beta)
        self.scores.assign_add(best_fbeta)
        self.count.assign_add(1)

    def result(self):
        return self.scores / (self.count + 1e-7)

    def reset_state(self):
        self.scores.assign(0)
        self.count.assign(0)