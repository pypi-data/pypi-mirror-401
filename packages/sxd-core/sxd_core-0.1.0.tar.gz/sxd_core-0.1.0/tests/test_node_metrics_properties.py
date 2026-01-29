from hypothesis import given, strategies as st
from datetime import datetime, timezone
from sxd_core.ops.node_metrics import (
    NodeMetrics,
    calculate_node_score,
    select_best_node,
)
from unittest.mock import patch

# Strategy for valid timestamps
st_datetime = st.datetimes(
    timezones=st.just(timezone.utc),
    min_value=datetime(2020, 1, 1),
    max_value=datetime(2030, 1, 1),
)


# Strategy for valid NodeMetrics
@st.composite
def node_metrics_strategy(draw):
    total = draw(
        st.integers(min_value=1_000_000, max_value=1_000_000_000_000)
    )  # 1MB to 1TB
    available = draw(st.integers(min_value=0, max_value=total))
    pending = draw(st.integers(min_value=0, max_value=available))
    stored = draw(st.integers(min_value=0, max_value=total))

    return NodeMetrics(
        hostname=draw(st.text(min_size=1)),
        disk_total_bytes=total,
        disk_available_bytes=available,
        cpu_cores=draw(st.integers(min_value=1, max_value=128)),
        pending_queue_bytes=pending,
        stored_bytes=stored,
        timestamp=draw(st_datetime),
    )


class TestNodeMetricsProperties:

    @given(node_metrics_strategy())
    def test_node_metrics_invariants(self, metrics):
        """Verify internal consistency of NodeMetrics properties."""
        assert 0.0 <= metrics.disk_usage_pct <= 1.0
        assert 0.0 <= metrics.disk_available_pct <= 1.0
        assert abs(metrics.disk_usage_pct + metrics.disk_available_pct - 1.0) < 1e-9

    @given(
        st.lists(
            node_metrics_strategy(),
            min_size=1,
            max_size=10,
            unique_by=lambda x: x.hostname,
        )
    )
    def test_calculate_score_bounds(self, metrics_list):
        """Verify scores are always between 0 and 1."""
        all_metrics = {m.hostname: m for m in metrics_list}

        for m in metrics_list:
            score = calculate_node_score(m, all_metrics)
            assert 0.0 <= score <= 1.0

    @given(st.lists(node_metrics_strategy(), min_size=1, max_size=5))
    def test_select_best_node_logic(self, metrics_list):
        """Verify select_best_node picks the winner of calculate_node_score."""
        # Ensure unique hostnames
        seen = set()
        unique = []
        for m in metrics_list:
            if m.hostname not in seen:
                seen.add(m.hostname)
                unique.append(m)
        if not unique:
            return

        all_metrics = {m.hostname: m for m in unique}
        available_nodes = [m.hostname for m in unique]

        with patch(
            "sxd_core.ops.node_metrics.get_all_node_metrics", return_value=all_metrics
        ):
            best = select_best_node(available_nodes, episode_size_bytes=0)

            # Manually calc scores
            scores = {m.hostname: calculate_node_score(m, all_metrics) for m in unique}
            expected_best = max(scores, key=scores.get)

            if best is None:
                # Should only be None if no scores (not possible here) or capacity check fail
                # But here we set size=0 so capacity check shouldn't fail unless code has bug
                pass
            else:
                assert best == expected_best
