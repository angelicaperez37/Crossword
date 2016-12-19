import collections
import math
import numpy as np
import string

class QLearningAlgorithm():

    def __init__(self, numWordFeatures, numLetterFeatures):
        #self.weights = np.matrix([0.0] * numWordFeatures)
        self.weights = np.matrix([[0.0]*numLetterFeatures]*26)
        # to get letter var's weight vector:
        # rowIdx = string.ascii_uppercase.index('[letter]')
        # self.weights[rowIdx]
        self.stepSize = 0.1
        self.discount = 1


    ''' performs Q-learning on a single CSP assignment by updating weights.
    # @featureVecs : dict of int keys and dict values
    #	- keys are the assignment orders
    #	- dict values hold the feature vectors for all possible assignments
    # @assignments : dict with int keys and letter/variable values
    # @maxFeatureVecs: dict with int keys and max feature vec lists
    '''

    def incorporateFeedback(self, featureVecs, assignments, domainPerc, solvedPerc):
        for t in range(len(assignments.keys())):
            a = assignments[t]
            if len(a) <= 1:
                continue
            wRowIdx = len(a)-1 #string.ascii_uppercase.index(a)
            reward = self.computeReward(domainPerc[t], solvedPerc)
            target = np.multiply(self.findMaxQ(featureVecs[t]),self.discount)+reward
            fv = [feat[1] for feat in featureVecs[t][a]]
            prediction = np.multiply(self.weights[wRowIdx], fv)
            temp = np.multiply(target-prediction, fv)
            self.weights[wRowIdx] += np.multiply(temp, self.stepSize)

    def incorporateFeedback_backtrack(self, featureVecs, numAssignments, maxAdditionalAssignments):
        for t in featureVecs.keys():
            print 'On trial ' + str(t)
            for a in numAssignments[t].keys():
                numValidAssignments = numAssignments[t][a]
                wRowIdx = string.ascii_uppercase.index(a)
                reward = 0
                if maxAdditionalAssignments[t] > 0:
                    reward = numAssignments[t][a]*1.0/maxAdditionalAssignments[t]
                target = np.multiply(self.findMaxQ(featureVecs[t]),self.discount)+reward
                fv = [feat[1] for feat in featureVecs[t][a]]
                prediction = np.multiply(self.weights[wRowIdx], fv)
                temp = np.multiply(target-prediction, fv)
                self.weights[wRowIdx] += np.multiply(temp, self.stepSize)
                #w = self.weights[wRowIdx]
                #self.weights[wRowIdx] = (w-w.min())/(w.max()-w.min())

            print self.weights

    def incorporateFeedback_hybrid(self, featureVecs, assignments, reward):
        for t in range(len(assignments.keys())):
            a = assignments[t]
            wRowIdx = 0
            weights = self.weights
            wRowIdx = string.ascii_uppercase.index(a)
            target = np.multiply(self.findMaxQ(featureVecs[t], a),self.discount)+reward
            fv = [feat[1] for feat in featureVecs[t][a]]
            prediction = np.multiply(weights[wRowIdx], fv)
            temp = np.multiply(target-prediction, fv)
            if len(a) == 1:
                self.letter_weights[wRowIdx] += np.multiply(temp, self.stepSize)
            else:
                self.word_weights[wRowIdx] += np.multiply(temp, self.stepSize)

    def computeReward(self, domainPerc, solvedPerc):
        reward = (domainPerc+solvedPerc)/2
        return reward

    def findMaxQ(self, featureVecs):
        maxQ = float("-inf")
        maxVec = None
        for x in featureVecs.keys():
            w = self.weights[string.ascii_uppercase.index(x)]
            fv = [feat[1] for feat in featureVecs[x]]
            vec = np.multiply(w, fv)
            Q = np.linalg.norm(vec)
            if Q > maxQ or maxVec == None:
                maxQ = Q
                maxVec = vec
        return maxVec
