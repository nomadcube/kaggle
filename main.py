from submission import submission
from pipeline import PipeLine
from models.mnb import LaplaceSmoothedMNB
import cProfile, pstats, StringIO
import sys

if __name__ == '__main__':
    train_file = sys.argv[1] if len(
        sys.argv) > 1 else '/Users/wumengling/PycharmProjects/kaggle/input_data/origin_train_subset.csv'
    exam_file = sys.argv[2] if len(
        sys.argv) > 2 else '/Users/wumengling/PycharmProjects/kaggle/input_data/test_subset.csv'
    exam_out_file = sys.argv[3] if len(
        sys.argv) > 3 else '/Users/wumengling/PycharmProjects/kaggle/output_data/submission.csv'
    pipeline = PipeLine(LaplaceSmoothedMNB, [80], [5])

    pr = cProfile.Profile()
    pr.enable()

    pipeline.run(train_file)
    print repr(pipeline)
    submission(exam_file, exam_out_file, pipeline)

    pr.disable()
    s = StringIO.StringIO()
    sortby = 'tottime'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print s.getvalue()
