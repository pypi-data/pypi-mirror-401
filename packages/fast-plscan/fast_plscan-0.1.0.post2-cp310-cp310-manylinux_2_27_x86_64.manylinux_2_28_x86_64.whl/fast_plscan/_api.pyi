from typing import Annotated

import numpy
from numpy.typing import NDArray


class CondensedTree:
    """CondensedTree contains a pruned dendrogram."""

    def __init__(self, parent: object, child: object, distance: object, child_size: object, cluster_rows: object) -> None:
        """
        Parameters
        ----------
        parent
            An array of parent cluster indices. Clusters are labelled
            with indices starting from the number of points.
        child
            An array of child node and cluster indices. Clusters are labelled
            with indices starting from the number of points.
        distance
            The distance at which the child side connects to the parent side.
        child_size
            The (weighted) size in the child side of the link.
        cluster_rows
            The row indices with a cluster as child.
        """

    @property
    def parent(self) -> Annotated[NDArray[numpy.uint32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array of parent cluster indices."""

    @property
    def child(self) -> Annotated[NDArray[numpy.uint32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array of child cluster indices."""

    @property
    def distance(self) -> Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array of distances."""

    @property
    def child_size(self) -> Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array of child sizes."""

    @property
    def cluster_rows(self) -> Annotated[NDArray[numpy.uint32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array of cluster row indices."""

    def __iter__(self) -> object: ...

    def __reduce__(self) -> tuple: ...

def compute_condensed_tree(linkage_tree: LinkageTree, minimum_spanning_tree: SpanningTree, num_points: int, min_cluster_size: float = 5.0, sample_weights: Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C')] | None = None) -> CondensedTree:
    """
    Prunes a linkage tree to create a condensed tree.

    Parameters
    ----------
    linkage_tree
        The input linkage tree. Must originate from and have the same size
        as the spanning tree.
    spanning_tree
        The input minimum spanning tree (sorted).
    min_cluster_size
        The minimum size of clusters to be included in the condensed tree.
        Default is 5.0.
    sample_weights
        The data point sample weights. If not provided, all
        points get an equal weight. Must have a value for each data point!

    Returns
    -------
    condensed_tree
        A CondensedTree with parent, child, distance, child_size,
        and cluster_rows arrays. The child_size array contains the
        (weighted) size of the child cluster, which is the sum of the
        sample weights for all points in the child cluster. The cluster_rows
        array contains the row indices with clusters as child.
    """

def get_dist(metric: str, **metric_kws) -> object:
    """
    Retrieves the specified distance metric callback.

    Parameters
    ----------
    metric
      The name of the metric to use. See :py:attr:`~plscan.PLSCAN.VALID_BALLTREE_METRICS`
      for a list of valid metrics.
    **metric_kws
      p: The order of the Minkowski distance. Required if `metric` is "minkowski".
      V: The variance vector for the standardized Euclidean distance. Required if
      `metric` is "seuclidean".
      VI: The inverse covariance matrix for the Mahalanobis distance. Required if
      `metric` is "mahalanobis".

    Returns
    -------
    dist
        The distance function callback. Its input arrays must be c-contiguous.
    """

class Labelling:
    """Labelling contains the cluster labels and probabilities."""

    def __init__(self, label: object, probability: object) -> None:
        """
        Parameters
        ----------
        label
            The data point cluster labels.
        persistence
            The data point cluster membership probabilities.
        """

    @property
    def label(self) -> Annotated[NDArray[numpy.int64], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with cluster labels."""

    @property
    def probability(self) -> Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with cluster membership probabilities."""

    def __iter__(self) -> object: ...

    def __reduce__(self) -> tuple: ...

def compute_cluster_labels(leaf_tree: LeafTree, condensed_tree: CondensedTree, selected_clusters: Annotated[NDArray[numpy.uint32], dict(shape=(None,), order='C', writable=False)], num_points: int) -> Labelling:
    """
    Computes cluster labels and membership probabilities for the points.

    Parameters
    ----------
    leaf_tree
        The input leaf tree.
    condensed_tree
        The input condensed tree.
    selected_clusters
        The condensed_tree parent IDs of the selected clusters.
    num_points
        The number of points in the condensed tree.

    Returns
    -------
    labelling
        The Labelling containing arrays for the cluster labels and
        membership probabilities. Labels -1 indicate points classified as
        noise.
    """

class LeafTree:
    """
    LeafTree lists information for the clusters in a condensed tree.

    Indexing with [cluster_id - num_points] gives information for the
    cluster with cluster_id.
    """

    def __init__(self, parent: object, min_distance: object, max_distance: object, min_size: object, max_size: object) -> None:
        """
        Parameters
        ----------
        parent
            The parent cluster IDs.
        min_distance
            The minimum distance at which the cluster ID exists in the
            condensed tree. The leaf-cluster represented by the cluster ID
            may exist at smaller distances because it can contain points of
            its descendants.
        max_distance
            The distance at which the cluster connects to its parent in the
            condensed tree and leaf tree.
        min_size
            The min_cluster_size at which the cluster becomes a leaf.
        max_size
            The min_cluster_size at which the cluster stops being a leaf.
        """

    @property
    def parent(self) -> Annotated[NDArray[numpy.uint32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with parent cluster IDs."""

    @property
    def min_distance(self) -> Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C', writable=False)]:
        """
        A 1D array with minimum leaf cluster distances. I.e., the minimum distance at which the cluster ID exists in the condensed tree. The leaf-cluster represented by the cluster ID may exist at smaller distances because it can contain points of its children.
        """

    @property
    def max_distance(self) -> Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with maximum leaf cluster distances."""

    @property
    def min_size(self) -> Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with minimum leaf cluster sizes."""

    @property
    def max_size(self) -> Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with maximum leaf cluster sizes."""

    def __iter__(self) -> object: ...

    def __reduce__(self) -> tuple: ...

def compute_leaf_tree(condensed_tree: CondensedTree, num_points: int, min_cluster_size: float = 5.0) -> LeafTree:
    """
    Computes a leaf tree from a condensed tree.

    Parameters
    ----------
    condensed_tree
        The input condensed tree.
    num_points
        The number of points in the dataset.
    min_cluster_size
        The minimum size of clusters to be included in the leaf tree.

    Returns
    -------
    leaf_tree
        A LeafTree containing parent, min_distance, max_distance, min_size,
        and max_size arrays. The min/max distance arrays contain each
        cluster's distance range. The min_size and max_size arrays contain
        the minimum and maximum min_cluster_size thresholds for which the
        clusters are leaves, respectively. Some clusters never become
        leaves, indicated by a min_size larger than the max_size.
    """

def apply_size_cut(leaf_tree: LeafTree, cut_size: float) -> Annotated[NDArray[numpy.uint32], dict(shape=(None,), order='C', writable=False)]:
    """
    Finds the cluster IDs for leaf-clusters that exist at the
    given cut_size threshold. The threshold is interpreted as a
    birth value in a left-open (birth, death] size interval.

    Parameters
    ----------
    leaf_tree
        The input leaf tree.
    size_cut
        The size threshold for selecting clusters. The threshold is
        interpreted as a birth value in a left-open (birth, death] size
        interval.

    Returns
    -------
    selected_clusters
        The cluster IDs for leaf-clusters that exist at the
        given cut_size threshold.
    """

def apply_distance_cut(leaf_tree: LeafTree, cut_distance: float) -> Annotated[NDArray[numpy.uint32], dict(shape=(None,), order='C', writable=False)]:
    """
    Finds the cluster IDs for clusters that exist at the given cut distance
    threshold.

    Parameters
    ----------
    leaf_tree
        The input leaf tree.
    distance_cut
        The distance threshold for selecting clusters.

    Returns
    -------
    selected_clusters
        The cluster IDs for clusters that exist at the given distance
        threshold.
    """

class LinkageTree:
    """LinkageTree contains a single-linkage dendrogram."""

    def __init__(self, parent: Annotated[NDArray[numpy.uint32], dict(shape=(None,), order='C', writable=False)], child: Annotated[NDArray[numpy.uint32], dict(shape=(None,), order='C', writable=False)], child_count: Annotated[NDArray[numpy.uint32], dict(shape=(None,), order='C', writable=False)], child_size: Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C', writable=False)]) -> None:
        """
        Parameters
        ----------
        parent
            An array of parent node and cluster indices. Clusters are
            labelled with indices starting from the number of points.
        child
            An array of child node and cluster indices. Clusters are labelled
            with indices starting from the number of points.
        child_count
            The number of points contained in the child side of the link.
        child_size
            The (weighted) size in the child side of the link.
        """

    @property
    def parent(self) -> Annotated[NDArray[numpy.uint32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with parent values."""

    @property
    def child(self) -> Annotated[NDArray[numpy.uint32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with child values."""

    @property
    def child_count(self) -> Annotated[NDArray[numpy.uint32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with child_count values."""

    @property
    def child_size(self) -> Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with child_size values."""

    def __iter__(self) -> object: ...

    def __reduce__(self) -> tuple: ...

def compute_linkage_tree(minimum_spanning_tree: SpanningTree, num_points: int, sample_weights: Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C')] | None = None) -> LinkageTree:
    """
    Constructs a LinkageTree containing a single-linkage
    dendrogram.

    Parameters
    ----------
    minimum_spanning_tree
        The SpanningTree containing the (sorted/partial) minimum spanning
        tree.
    num_points
        The number of data points in the data set.
    sample_weights
        The data point sample weights. If not provided, all points
        get an equal weight.

    Returns
    -------
    tree
        A LinkageTree containing the parent, child, child_count,
        and child_size arrays of the single-linkage dendrogram.
        Count refers to the number of data points in the child
        cluster. Size refers to the (weighted) size of the child
        cluster, which is the sum of the sample weights for all
        points in the child cluster.
    """

class PersistenceTrace:
    """PersistenceTrace lists the persistences per min_cluster_size."""

    def __init__(self, min_size: object, persistence: object) -> None:
        """
        Parameters
        ----------
        min_size
            The minimum cluster sizes at which leaf-clusters start to exist.
        persistence
            The persistence sum for the leaf-clusters that exist at the
            minimum cluster sizes.
        """

    @property
    def min_size(self) -> Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with minimum cluster sizes."""

    @property
    def persistence(self) -> Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with total persistence values."""

    def __iter__(self) -> object: ...

    def __reduce__(self) -> tuple: ...

def compute_size_persistence(leaf_tree: LeafTree) -> PersistenceTrace:
    """
    Computes the total min_cluster_size persistence trace.

    Parameters
    ----------
    leaf_tree
        The input leaf tree.

    Returns
    -------
    persistence_trace
        A PersistenceTrace containing arrays for the minimum cluster size
        and total persistence values. The min_size array contains all unique
        min_cluster_sizes at which clusters become leaves. The persistence
        array contains the total persistence of leaf clusters at those
        minimum size thresholds.
    """

def compute_distance_persistence(leaf_tree: LeafTree, condensed_tree: CondensedTree, num_points: int) -> PersistenceTrace:
    """
    Computes the total mutual reachability distance persistence trace.

    Parameters
    ----------
    leaf_tree
        The input leaf tree.
    condensed_tree
        The input condensed tree.
    num_points
        The number of points in the condensed tree.

    Returns
    -------
    persistence_trace
        A PersistenceTrace containing arrays for the minimum cluster size
        and total persistence values. The min_size array contains all unique
        min_cluster_sizes at which clusters become leaves. The persistence
        array contains the total persistence of leaf clusters at those
        minimum size thresholds.
    """

def compute_density_persistence(leaf_tree: LeafTree, condensed_tree: CondensedTree, num_points: int) -> PersistenceTrace:
    """
    Computes the total mutual reachability density persistence trace.

    Parameters
    ----------
    leaf_tree
        The input leaf tree.
    condensed_tree
        The input condensed tree.
    num_points
        The number of points in the condensed tree.

    Returns
    -------
    persistence_trace
        A PersistenceTrace containing arrays for the minimum cluster size
        and total persistence values. The min_size array contains all unique
        min_cluster_sizes at which clusters become leaves. The persistence
        array contains the total persistence of leaf clusters at those
        minimum size thresholds.
    """

def compute_size_distance_bi_persistence(leaf_tree: LeafTree, condensed_tree: CondensedTree, num_points: int) -> PersistenceTrace:
    """
    Computes a bi-persistence trace for over min_cluster_size and
    mutual reachability distances.

    Parameters
    ----------
    leaf_tree
        The input leaf tree.
    condensed_tree
        The input condensed tree.
    num_points
        The number of points in the condensed tree.

    Returns
    -------
    persistence_trace
        A PersistenceTrace containing arrays for the minimum cluster size
        and total persistence values. The min_size array contains all unique
        min_cluster_sizes at which clusters become leaves. The persistence
        array contains the total bi-persistence of leaf clusters at those
        minimum size thresholds.
    """

def compute_size_density_bi_persistence(leaf_tree: LeafTree, condensed_tree: CondensedTree, num_points: int) -> PersistenceTrace:
    """
    Computes a bi-persistence trace for over min_cluster_size and
    mutual reachability densities.

    Parameters
    ----------
    leaf_tree
        The input leaf tree.
    condensed_tree
        The input condensed tree.
    num_points
        The number of points in the condensed tree.

    Returns
    -------
    persistence_trace
        A PersistenceTrace containing arrays for the minimum cluster size
        and total persistence values. The min_size array contains all unique
        min_cluster_sizes at which clusters become leaves. The persistence
        array contains the total bi-persistence of leaf clusters at those
        minimum size thresholds.
    """

def compute_distance_icicles(leaf_tree: LeafTree, condensed_tree: CondensedTree, num_points: int) -> tuple[list[Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C')]], list[Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C')]]]:
    """
    Computes size--distance traces for the LeafTree plot.

    Parameters
    ----------
    leaf_tree
        The input leaf tree.
    condensed_tree
        The input condensed tree.
    num_points
        The number of points in the condensed tree.

    Returns
    -------
    sizes
        The icicle min cluster sizes (births in (birth, death])).
    stabilities
        The icicle stabilities.
    """

def compute_density_icicles(leaf_tree: LeafTree, condensed_tree: CondensedTree, num_points: int) -> tuple[list[Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C')]], list[Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C')]]]:
    """
    Computes size--density traces for the LeafTree plot.

    Parameters
    ----------
    leaf_tree
        The input leaf tree.
    condensed_tree
        The input condensed tree.
    num_points
        The number of points in the condensed tree.

    Returns
    -------
    sizes
        The icicle min cluster sizes (births in (birth, death])).
    stabilities
        The icicle stabilities.
    """

class NodeData:
    """NodeData represents nodes in sklearn KDTrees and BallTrees."""

    def __init__(self, idx_start: int, idx_end: int, is_leaf: int, radius: float) -> None:
        """
        Parameters
        ----------
        idx_start
            The starting index of the node in the tree.
        idx_end
            The ending index of the node in the tree.
        is_leaf
            A flag indicating whether the node is a leaf (1) or not (0).
        radius
            The radius of the node, used in BallTrees to define the
            hypersphere that contains the points in the node.
        """

    @property
    def idx_start(self) -> int:
        """The starting index of the node in the tree."""

    @property
    def idx_end(self) -> int:
        """The ending index of the node in the tree."""

    @property
    def is_leaf(self) -> int:
        """A flag indicating whether the node is a leaf (1) or not (0)."""

    @property
    def radius(self) -> float:
        """
        The radius of the node, used in BallTrees to define the hypersphere that contains the points in the node.
        """

    def __iter__(self) -> object: ...

    def __reduce__(self) -> tuple: ...

class SpaceTree:
    """SpaceTree represents sklearn KDTrees and BallTrees."""

    def __init__(self, data: Annotated[NDArray[numpy.float32], dict(shape=(None, None), order='C', writable=False)], idx_array: Annotated[NDArray[numpy.int64], dict(shape=(None,), order='C', writable=False)], node_data: Annotated[NDArray[numpy.float64], dict(shape=(None,), order='C', writable=False)], node_bounds: Annotated[NDArray[numpy.float32], dict(shape=(None, None, None), order='C', writable=False)]) -> None:
        """
        Parameters
        ----------
        data
            The data feature vectors.
        idx_array
            The tree's index array mapping points to tree nodes.
        node_data
            A float64 view into the structured :py:class:`~NodeData` array.
        node_bounds
            The node bounds, a 3D array (x, num_nodes, num_features),
            representing the min and max bounds of each node in the feature
            space.
        """

    @property
    def data(self) -> Annotated[NDArray[numpy.float32], dict(shape=(None, None), order='C', writable=False)]:
        """A 2D array with feature vectors."""

    @property
    def idx_array(self) -> Annotated[NDArray[numpy.int64], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array mapping nodes to data points."""

    @property
    def node_data(self) -> Annotated[NDArray[numpy.float64], dict(shape=(None,), order='C', writable=False)]:
        """A 1D float64 view into a node data array."""

    @property
    def node_bounds(self) -> Annotated[NDArray[numpy.float32], dict(shape=(None, None, None), order='C', writable=False)]:
        """A 3D array with node bounds."""

    def __iter__(self) -> object: ...

    def __reduce__(self) -> tuple: ...

def check_node_data(node_data: Annotated[NDArray[numpy.float64], dict(shape=(None,), order='C', writable=False)]) -> list[NodeData]:
    """
    Converts float64 node_data view to a list of NodeData objects.
    This function is used in tests to check whether the node data
    conversion works correctly!

    Parameters
    ----------
    node_data
        A flat float64 array view containing :py:class:`~NodeData`.

    Returns
    -------
    copied_data
        A list of :py:class:`~NodeData` objects created from the input
        array.
    """

def kdtree_query(tree: SpaceTree, num_neighbors: int, metric: str, metric_kws: dict) -> SparseGraph:
    """
    Performs a k-nearest neighbors query on a SpaceTree.

    Parameters
    ----------
    tree
        The SpaceTree to query (must be a KDTree!).
    num_neighbors
        The number of nearest neighbors to find.
    metric
        The distance metric to use. Supported metrics are listed in
        :py:attr:`~plscan.PLSCAN.VALID_KDTREE_METRICS`.
    metric_kws
        Additional keyword arguments for the distance function, such as
        the Minkowski distance parameter `p` for the "minkowski" metric.

    Returns
    -------
    knn
        A sparse graph containing the distance-sorted nearest neighbors for
        each point.
    """

def balltree_query(tree: SpaceTree, num_neighbors: int, metric: str, metric_kws: dict) -> SparseGraph:
    """
    Performs a k-nearest neighbors query on a SpaceTree.

    Parameters
    ----------
    tree
        The SpaceTree to query (must be a BallTree!).
    num_neighbors
        The number of nearest neighbors to find.
    metric
        The distance metric to use. Supported metrics are listed in
        :py:attr:`~plscan.PLSCAN.VALID_BALLTREE_METRICS`.
    metric_kws
        Additional keyword arguments for the distance function, such as
        the Minkowski distance parameter `p` for the "minkowski" metric.

    Returns
    -------
    knn
        A sparse graph containing the distance-sorted nearest neighbors for
        each point.
    """

class SpanningTree:
    """SpanningTree contains a sorted minimum spanning tree (MST)."""

    def __init__(self, parent: object, child: object, distance: object) -> None:
        """
        Parameters
        ----------
        parent
            An array of parent node indices.
        child
            An array of child node indices.
        distance
            An array of distances between the nodes.
        """

    @property
    def parent(self) -> Annotated[NDArray[numpy.uint32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with parent values."""

    @property
    def child(self) -> Annotated[NDArray[numpy.uint32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with child values."""

    @property
    def distance(self) -> Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with distance values."""

    def __iter__(self) -> object: ...

    def __reduce__(self) -> tuple: ...

def extract_spanning_forest(graph: SparseGraph) -> SpanningTree:
    """
    Extracts a minimum spanning forest from a sparse graph.

    Parameters
    ----------
    graph
        The input sparse graph.

    Returns
    -------
    spanning_tree
        The computed spanning forest.
    """

def compute_spanning_tree_kdtree(tree: SpaceTree, knn: SparseGraph, core_distances: Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C')], metric: str, metric_kws: dict) -> SpanningTree:
    """
    Computes a minimum spanning tree (MST) using a k-d tree.

    Parameters
    ----------
    tree
        The kdtree structure.
    knn
        The k-nearest neighbors graph.
    core_distances
        The core distances for each point.
    metric
        The distance metric to use. Supported metrics are listed in
        :py:attr:`~plscan.PLSCAN.VALID_KDTREE_METRICS`.
    metric_kws
        Additional keyword arguments for the distance function, such as
        the Minkowski distance parameter `p` for the "minkowski" metric.

    Returns
    -------
    spanning_tree
        The computed minimum spanning tree.
    """

def compute_spanning_tree_balltree(tree: SpaceTree, knn: SparseGraph, core_distances: Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C')], metric: str, metric_kws: dict) -> SpanningTree:
    """
    Computes a minimum spanning tree (MST) using a ball tree.

    Parameters
    ----------
    tree
        The balltree structure.
    knn
        The k-nearest neighbors graph.
    core_distances
        The core distances for each point.
    metric
        The distance metric to use. Supported metrics are listed in
        :py:attr:`~plscan.PLSCAN.VALID_BALLTREE_METRICS`.
    metric_kws
        Additional keyword arguments for the distance function, such as
        the Minkowski distance parameter `p` for the "minkowski" metric.

    Returns
    -------
    spanning_tree
        The computed minimum spanning tree.
    """

class SparseGraph:
    """SparseGraph contains a (square) distance matrix in CSR format."""

    def __init__(self, data: object, indices: object, indptr: object) -> None:
        """
        Parameters
        ----------
        data
            An array of distances.
        indices
            An array of column indices.
        indptr
            The CSR indptr array.
        """

    @property
    def data(self) -> Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with data values."""

    @property
    def indices(self) -> Annotated[NDArray[numpy.int32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with indices values."""

    @property
    def indptr(self) -> Annotated[NDArray[numpy.int32], dict(shape=(None,), order='C', writable=False)]:
        """A 1D array with indptr values."""

    def __iter__(self) -> object: ...

    def __reduce__(self) -> tuple: ...

def extract_core_distances(graph: SparseGraph, min_samples: int = 5, is_sorted: bool = False) -> Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C')]:
    """
    Extracts core distances from a sparse graph.

    Parameters
    ----------
    graph
          The sparse graph to extract core distances from.
    min_samples
          The number of nearest neighbors to consider for core distance.
    is_sorted
          Whether the rows of the graph are sorted by distance.

    Returns
    -------
    core_distances
          An array of core distances.
    """

def compute_mutual_reachability(graph: SparseGraph, core_distances: Annotated[NDArray[numpy.float32], dict(shape=(None,), order='C')]) -> SparseGraph:
    """
    Applies core distances to a sparse graph to compute mutual
    reachability.

    Parameters
    ----------
    graph
          The sparse graph to extract core distances from.
    core_distances
          An array of core distances, one for each point in the graph.

    Returns
    -------
    mutual_graph
          A new sparse graph with mutual reachability distances. Rows are
          sorted by mutual reachability distance.
    """

def get_max_threads() -> int:
    """Returns the default number of OpenMP threads used."""

def set_num_threads(num_threads: int) -> None:
    """
    Sets the default number of OpenMP threads to use.

    Parameters
    ----------
    num_threads : int
          The number of threads to set.
    """
