from tiny_pii.pii_aggreagator import PIIAggregator
from tiny_pii.pii_filter import PIIFilter
from tiny_pii.pii_mask import PIIMasker


def test_aggreagate_filter(list_before_aggregation, sample_text_jt):
    aggregated = PIIAggregator.aggregate(list_before_aggregation)
    assert len(aggregated) == 6

    filtered = PIIFilter.filter_and_resolve_overlaps(aggregated)
    assert len(filtered) == 5
    print(filtered)

    masked = PIIMasker.mask_text(sample_text_jt, filtered)
    print(masked)
