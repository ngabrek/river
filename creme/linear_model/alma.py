import collections
import math

from creme import base
from creme import utils


__all__ = ['ALMAClassifier']


class ALMAClassifier(base.BinaryClassifier):
    """Approximate Large Margin Algorithm (ALMA).

    Parameters:
        p (float)
        alpha (float)
        B (float)
        C (float)

    Example:

        ::

            >>> from creme import datasets
            >>> from creme import metrics
            >>> from creme import model_selection
            >>> from creme import optim
            >>> from creme import preprocessing

            >>> X_y = datasets.Phishing()

            >>> model = (
            ...     preprocessing.StandardScaler() |
            ...     linear_model.ALMAClassifier()
            ... )

            >>> metric = metrics.Accuracy()

            >>> model_selection.progressive_val_score(X_y, model, metric)

    References:
        1. `Gentile, Claudio. "A new approximate maximal margin classification algorithm." Journal of Machine Learning Research 2.Dec (2001): 213-242.
 <http://www.jmlr.org/papers/volume2/gentile01a/gentile01a.pdf>`_

    """

    def __init__(self, p=2, alpha=.9, B=1 / .9, C=2 ** .5):
        self.p = p
        self.alpha = alpha
        self.B = B
        self.C = C
        self.w = collections.defaultdict(float)
        self.k = 1

    def _raw_dot(self, x):
        return utils.math.dot(x, self.w)

    def predict_proba_one(self, x):
        yp = utils.math.sigmoid(self._raw_dot(x))
        return {False: 1 - yp, True: yp}

    def fit_one(self, x, y):

        # Convert 0 to -1
        y = int(y or -1)

        gamma = self.B * math.sqrt(self.p - 1) / math.sqrt(self.k)

        if y * self._raw_dot(x) < (1 - self.alpha) * gamma:

            eta = self.C / (math.sqrt(self.p - 1) * math.sqrt(self.k))

            for i, xi in x.items():
                self.w[i] += eta * y * xi

            norm = utils.math.norm(self.w, order=self.p)

            for i in x:
                self.w[i] /= max(1, norm)

            self.k += 1

        return self
