__author__ = 'Guilherme Matsumoto'

from abc import ABCMeta, abstractmethod

class BaseInstanceStream(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def estimatedRemainingInstances(self):
        pass

    @abstractmethod
    def hasMoreInstances(self):
        pass

    @abstractmethod
    def nextInstance(self):
        pass

    @abstractmethod
    def isRestartable(self):
        pass

    @abstractmethod
    def restart(self):
        pass

    @abstractmethod
    def nextInstanceMiniBatch(self):
        pass

    @abstractmethod
    def hasMoreMiniBatch(self):
        pass

    @abstractmethod
    def getNumNominalAttributes(self):
        pass

    @abstractmethod
    def getNumNumericalAttributes(self):
        pass

    @abstractmethod
    def getNumValuesPerNominalAttribute(self):
        pass

    @abstractmethod
    def getNumClasses(self):
        pass

    @abstractmethod
    def getAttributesHeader(self):
        pass

    @abstractmethod
    def getClassesHeader(self):
        pass