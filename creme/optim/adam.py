import collections

from . import base


__all__ = ['Adam']


class Adam(base.Optimizer):
    """Adam optimizer.

    Example:

        ::

            >>> from creme import compose
            >>> from creme import linear_model
            >>> from creme import metrics
            >>> from creme import model_selection
            >>> from creme import optim
            >>> from creme import preprocessing
            >>> from creme import stream
            >>> from sklearn import datasets

            >>> X_y = stream.iter_sklearn_dataset(
            ...     load_dataset=datasets.load_breast_cancer,
            ...     shuffle=True,
            ...     random_state=42
            ... )
            >>> optimiser = optim.Adam()
            >>> model = compose.Pipeline([
            ...     ('scale', preprocessing.StandardScaler()),
            ...     ('learn', linear_model.LogisticRegression(optimiser))
            ... ])
            >>> metric = metrics.F1Score()

            >>> model_selection.online_score(X_y, model, metric)
            F1Score: 0.960894

    """

    def __init__(self, lr=0.1, beta_1=0.9, beta_2=0.999, eps=1e-8):
        super().__init__(lr)
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.eps = eps
        self.m = collections.defaultdict(float)
        self.v = collections.defaultdict(float)

    def update_weights_with_gradient(self, w, g):

        for i, gi in g.items():
            self.m[i] = self.beta_1 * self.m[i] + (1 - self.beta_1) * gi
            self.v[i] = self.beta_2 * self.v[i] + (1 - self.beta_2) * gi ** 2
            m = self.m[i] / (1 - self.beta_1 ** (self.n_iterations + 1))
            v = self.v[i] / (1 - self.beta_2 ** (self.n_iterations + 1))
            w[i] -= self.learning_rate * m / (v ** 0.5 + self.eps)

        return w
