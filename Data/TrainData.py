import io
from tf_idf_swig.tf_idf import tf_idf, doc_term_val_t


class _Response:
    """Represent Y in training data."""

    def __init__(self, data):
        if not isinstance(data, dict):
            raise TypeError('Y must be of type dict.')
        self.data = data
        self.remapped_data = dict()
        self.remapping_relation = dict()

    def remap(self, train_remapping_rel=None):
        """Map original y value to its hash code."""
        if not train_remapping_rel:
            for y_index, y_key in enumerate(self.data.keys()):
                original_y = self.data[y_key]
                self.remapped_data[y_key] = y_index
                self.remapping_relation[original_y] = y_index
        else:
            for y_key in self.data.keys():
                original_y = self.data[y_key]
                self.remapped_data[y_key] = train_remapping_rel[original_y]
                self.remapping_relation = train_remapping_rel
        return self


class _Variable:
    """Represent X in training data."""

    def __init__(self, data):
        if not isinstance(data, dict):
            raise TypeError('X must be of type dict.')
        self.data = data
        self.dim_reduction_data = dict()

    def dim_reduction(self, threshold):
        """Use tf-idf to perform dimension reduction."""
        self.dim_reduction_data = dict(tf_idf(doc_term_val_t(self.data), threshold))
        for k in self.dim_reduction_data:
            self.dim_reduction_data[k] = dict(self.dim_reduction_data[k])
        return self

    def _feature_count(self):
        """Count distinct features in the training data."""
        feature_set = set()
        for instance_index in self.dim_reduction_data.keys():
            for feature in self.dim_reduction_data[instance_index].keys():
                feature_set.add(feature)
        return len(feature_set)

    def __len__(self):
        return len(self.data)


class TrainData:
    """Represent train data."""

    def __init__(self, train_data_path):
        y_dict, x_dict = self._get_y_x(train_data_path)
        self.y = _Response(y_dict)
        self.x = _Variable(x_dict)

    def _get_y_x(self, train_data_path):
        """Get y and x data from file lines."""
        y_res = dict()
        x_res = dict()
        for index, line in enumerate(io.open(train_data_path, 'r').readlines()):
            x_res[index] = dict()
            tmp_y, tmp_x = line.strip().split(' ', 1)
            y_res[index] = tmp_y
            for column in tmp_x.split(' '):
                feat, val = column.split(':')
                feat = int(feat)
                val = float(val)
                x_res[index][feat] = val
        return y_res, x_res

    def description(self):
        return len(self.x), self.x._feature_count()

