import numpy
import cv2
import scipy.io
import scipy.sparse

class HistogramClassifier(object):

    # init
    def __init__(self):
        # public
        self.verbose = False
        self.minimumSimilarityForPositiveLabel = 0.075
        # protected
        self._channels = range(3)
        self._histSize = [256] * 3
        self._ranges = [0, 255] * 3
        self._references = {}

    # protected
    def _createNomalizedHist(self, image, sparse):
        # Create the histogram
        hist = cv2.calcHist([image], self._channels, None, self._histSize, self._ranges)

        # Nomalize the histgram
        hist[:] = hist * (1.0 / numpy.sum(hist))

        # Convert the histgram to one colum for efficient storage
        hist = hist.reshape(16777216, 1)

        if sparse:
            # Convert the histogram to a sparse martrix
            hist = scipy.sparse.csc_matrix(hist)

        return hist

    # public
    def addReference(self, image, label):
        hist = self._createNomalizedHist(image, True)
        if label not in self._references:
            self._references[label] = [hist]
        else:
            self._references[label] += [hist]

    # public
    def addReferenceFromFile(self, path, label):
        image = cv2.imread(path, cv2.IMREAD_COLOR)
        self.addReference(image, label)

    # public
    def classify(self, queryImage, queryImageName = None):
        queryHist = self._createNomalizedHist(queryImage, False)
        bestLabel = 'Unknown'
        bestSimilarity = self.minimumSimilarityForPositiveLabel

        if self.verbose:
            print '================================================'
            if queryImageName is not None:
                print 'Query image: '
                print '%s' % queryImageName
                print 'Mean similarity to reference images by label: '
        for label, referenceHists in self._references.iteritems():
            similarity = 0.0
            for referenceHist in referenceHists:
                similarity += numpy.sum(numpy.minimum(referenceHist.todense(), queryHist))
            similarity /= len(referenceHists)
            if self.verbose:
                print '%8f %s ' % (similarity, label)
            if similarity > bestSimilarity:
                bestSimilarity = similarity
                bestLabel = label
            if self.verbose:
                print '================================================'

        return bestLabel

    # public
    def classifyFromFile(self, path, queryImageName = None):
        if queryImageName is None:
            queryImageName = path
        queryImage = cv2.imread(path, cv2.IMREAD_COLOR)
        return self.classify(queryImage, queryImageName)

    # public
    def serialize(self, path, compressd = False):
        with open(path, 'wb') as fwb:
            scipy.io.savemat(fwb, self._references, do_compression = compressd)

    # public
    def deserialize(self, path):
        with open(path, 'rb') as frb:
            self._references = scipy.io.loadmat(frb)
            for key in self._references.keys():
                val = self._references[key]
                if not isinstance(val, numpy.ndarray):
                    del self._references[key]
                    continue

                # The serializer wraps the data in an extra array.
                # Unwrap the data.
                self._references[key] = val[0]



def main():
    classifier = HistogramClassifier()
    classifier.verbose = True

    # 'Stalinist, interior' reference images
    classifier.addReferenceFromFile(
        'images/communal_apartments_01.jpg',
        'Stalinist, interior')
    classifier.addReferenceFromFile(
        'images/communal_apartments_04.jpg',
        'Stalinist, interior')
    classifier.addReferenceFromFile(
        'images/communal_apartments_13.jpg',
        'Stalinist, interior')
    classifier.addReferenceFromFile(
        'images/communal_apartments_19.jpg',
        'Stalinist, interior')
    classifier.addReferenceFromFile(
        'images/magangue_room.jpg',
        'Stalinist, interior')
    classifier.addReferenceFromFile(
        'images/moscow_concrete_hall.jpg',
        'Stalinist, interior')
    classifier.addReferenceFromFile(
        'images/moscow_flat_30.jpg',
        'Stalinist, interior')
    classifier.addReferenceFromFile(
        'images/moscow_flat_31.jpg',
        'Stalinist, interior')
    classifier.addReferenceFromFile(
        'images/moscow_flat_36.jpg',
        'Stalinist, interior')
    classifier.addReferenceFromFile(
        'images/moscow_flat_43.jpg',
        'Stalinist, interior')

    # 'Stalinist, exterior' reference images
    classifier.addReferenceFromFile(
        'images/murmansk_exterior.jpg',
        'Stalinist, exterior')
    classifier.addReferenceFromFile(
        'images/norilsk_exterior.jpg',
        'Stalinist, exterior')
    classifier.addReferenceFromFile(
        'images/st_petersburg_exterior.jpg',
        'Stalinist, exterior')

    # 'Luxury, interior' reference images
    classifier.addReferenceFromFile(
        'images/dubai_damac_heights.jpg',
        'Luxury, interior')
    classifier.addReferenceFromFile(
        'images/kazan_jacuzzi.jpg',
        'Luxury, interior')
    classifier.addReferenceFromFile(
        'images/london_holland_park.jpg',
        'Luxury, interior')
    classifier.addReferenceFromFile(
        'images/miami_beach.jpg',
        'Luxury, interior')
    classifier.addReferenceFromFile(
        'images/miami_moroccan_inspired.jpg',
        'Luxury, interior')
    classifier.addReferenceFromFile(
        'images/panama_casa_del_horno.jpg',
        'Luxury, interior')
    classifier.addReferenceFromFile(
        'images/panama_pacific_point.jpg',
        'Luxury, interior')
    classifier.addReferenceFromFile(
        'images/sydney_potts_point.jpg',
        'Luxury, interior')

    # 'Luxury, exterior' reference images
    classifier.addReferenceFromFile(
        'images/buenos_aires_recoleta_exterior.jpg',
        'Luxury, exterior')
    classifier.addReferenceFromFile(
        'images/herradura_exterior.jpg',
        'Luxury, exterior')
    classifier.addReferenceFromFile(
        'images/nuevo_vallarta_grand_maya.jpg',
        'Luxury, exterior')
    classifier.addReferenceFromFile(
        'images/panama_trump_exterior.jpg',
        'Luxury, exterior')

    classifier.serialize('classifier.mat')
    classifier.deserialize('classifier.mat')
    classifier.classifyFromFile('images/dubai_damac_heights.jpg')
    classifier.classifyFromFile('images/communal_apartments_01.jpg')


if __name__ == '__main__':
    main()
