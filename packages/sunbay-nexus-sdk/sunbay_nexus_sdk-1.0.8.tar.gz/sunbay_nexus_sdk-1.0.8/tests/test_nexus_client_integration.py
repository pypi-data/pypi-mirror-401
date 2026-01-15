"""
Integration tests for NexusClient (all APIs).

这些测试会真实调用 Sunbay Nexus 的 HTTP 接口，语义上等价于 Java 版本的 NexusClientTest。
默认使用 pytest，并且带有跳过标记，避免在本地未配置好测试环境时误打线上。

注意：这些测试只验证接口可以正常调用和响应可以正确解析，不要求接口返回 code=0。
业务错误（如交易不存在等）是正常的，只要SDK能正确调用接口并解析响应即可。
"""

import logging
import time
from dataclasses import asdict, is_dataclass
from datetime import datetime, timedelta, timezone

import pytest

from sunbay_nexus_sdk import (
    NexusClient,
    SunbayBusinessError,
    SunbayNetworkError,
    TransactionStatus,
    TransactionType,
)
from sunbay_nexus_sdk.models.common import AuthAmount, PostAuthAmount, RefundAmount, SaleAmount
from sunbay_nexus_sdk.models.request import (
    AbortRequest,
    AuthRequest,
    BatchCloseRequest,
    BatchQueryRequest,
    ForcedAuthRequest,
    IncrementalAuthRequest,
    PostAuthRequest,
    QueryRequest,
    RefundRequest,
    SaleRequest,
    TipAdjustRequest,
    VoidRequest,
)


# 注意：这里的参数与 Java 版本的 NexusClientTest 保持一致，
# 仅用于测试环境，不用于生产环境。

TEST_API_KEY = "mfgyn0hvs9teofvuad03jkwvmtrdm2sb"
TEST_BASE_URL = "https://open.sunbay.dev"

TEST_APP_ID = "test_sm6par3xf4d3tkum"
TEST_MERCHANT_ID = "M1254947005"
TEST_TERMINAL_SN = "TESTSN1764580772062"

# Java NexusClientTest testQuery 中使用的请求 ID
EXISTING_TRANSACTION_REQUEST_ID = "PAY_REQ_1765785418963"

# Dedicated logger for integration tests
test_logger = logging.getLogger("sunbay_nexus_sdk.tests.integration")


def _iso8601_after_minutes(minutes: int) -> str:
    # Align with Java test implementation:
    # ZonedDateTime.now().plusMinutes(10).format("yyyy-MM-dd'T'HH:mm:ssXXX")
    dt = datetime.now().astimezone() + timedelta(minutes=minutes)
    # ISO 8601 with timezone offset like +08:00
    return dt.isoformat(timespec="seconds")


def _build_client() -> NexusClient:
    return NexusClient(
        api_key=TEST_API_KEY,
        base_url=TEST_BASE_URL,
    )


def test_sale_integration():
    """
    真正调用 sale 接口的集成测试，用于验证 NexusClient.sale 整条链路。
    """
    client = _build_client()

    amount = SaleAmount(order_amount=22200, price_currency="USD")  # 222.00 USD = 22200 cents
    request = SaleRequest(
        app_id=TEST_APP_ID,
        merchant_id=TEST_MERCHANT_ID,
        reference_order_id=f"ORDER{int(time.time() * 1000)}",
        transaction_request_id=f"PAY_REQ_{int(time.time() * 1000)}",
        amount=amount,
        description="Integration test sale",
        terminal_sn=TEST_TERMINAL_SN,
        attach='{"storeId":"STORE001","tableNo":"T05"}',
        notify_url="https://merchant.com/notify",
        time_expire=_iso8601_after_minutes(10),
    )

    try:
        response = client.sale(request)
        assert response is not None

        # 只打印关键字段，避免整包输出过长。
        test_logger.info(
            "Sale integration parsed by SDK - code=%s, msg=%s, trace_id=%s, "
            "transaction_id=%s, reference_order_id=%s, transaction_request_id=%s",
            getattr(response, "code", None),
            getattr(response, "msg", None),
            getattr(response, "trace_id", None),
            getattr(response, "transaction_id", None),
            getattr(response, "reference_order_id", None),
            getattr(response, "transaction_request_id", None),
        )
    except SunbayNetworkError as e:
        pytest.fail(f"Network error during sale integration test: {e}")
    except SunbayBusinessError as e:
        test_logger.info("Sale integration business error (expected): code=%s, msg=%s", e.code, e)


def test_query_integration():
    """
    真正调用 query 接口的集成测试，用于验证 NexusClient.query 整条链路。
    前提是你已经有一笔已存在的交易 ID 或请求 ID。
    """
    client = _build_client()

    request = QueryRequest(
        app_id=TEST_APP_ID,
        merchant_id=TEST_MERCHANT_ID,
        transaction_request_id=EXISTING_TRANSACTION_REQUEST_ID,
    )

    try:
        response = client.query(request)
        assert response is not None

        # Verify enum values match API response
        if response.transaction_status:
            # API returns code (e.g., "S"), verify it matches enum
            status_enum = TransactionStatus(response.transaction_status)
            test_logger.info("Transaction status enum verification: %s -> %s", response.transaction_status, status_enum)

        if response.transaction_type:
            # API returns code (e.g., "SALE"), verify it matches enum
            type_enum = TransactionType(response.transaction_type)
            test_logger.info("Transaction type enum verification: %s -> %s", response.transaction_type, type_enum)

        test_logger.info(
            "Query integration parsed by SDK - code=%s, msg=%s, trace_id=%s, "
            "transaction_id=%s, transaction_request_id=%s, reference_order_id=%s, "
            "transaction_status=%s, transaction_type=%s",
            getattr(response, "code", None),
            getattr(response, "msg", None),
            getattr(response, "trace_id", None),
            getattr(response, "transaction_id", None),
            getattr(response, "transaction_request_id", None),
            getattr(response, "reference_order_id", None),
            getattr(response, "transaction_status", None),
            getattr(response, "transaction_type", None),
        )
    except SunbayNetworkError as e:
        pytest.fail(f"Network error during query integration test: {e}")
    except SunbayBusinessError as e:
        test_logger.info("Query integration business error (expected): code=%s, msg=%s", e.code, e)


def test_abort_integration():
    """
    真正调用 abort 接口的集成测试，用于验证 NexusClient.abort 整条链路。
    前提是你已经有一笔可以 abort 的交易（通常是 PROCESSING 状态的交易）。
    """
    client = _build_client()

    request = AbortRequest(
        app_id=TEST_APP_ID,
        merchant_id=TEST_MERCHANT_ID,
        original_transaction_request_id=EXISTING_TRANSACTION_REQUEST_ID,
        terminal_sn=TEST_TERMINAL_SN,
        description="Integration test abort",
        attach='{"reason":"Test abort"}',
    )

    try:
        response = client.abort(request)
        assert response is not None
        # If we reach here, code == "0" (success), no need to check is_success()

        test_logger.info(
            "Abort integration parsed by SDK - code=%s, msg=%s, trace_id=%s, "
            "original_transaction_id=%s, original_transaction_request_id=%s",
            getattr(response, "code", None),
            getattr(response, "msg", None),
            getattr(response, "trace_id", None),
            getattr(response, "original_transaction_id", None),
            getattr(response, "original_transaction_request_id", None),
        )
    except SunbayNetworkError as e:
        pytest.fail(f"Network error during abort integration test: {e}")
    except SunbayBusinessError as e:
        # Business error is acceptable, just log it
        test_logger.info("Abort integration business error (expected): code=%s, msg=%s", e.code, e)


def test_auth_integration():
    """
    真正调用 auth 接口的集成测试，用于验证 NexusClient.auth 整条链路。
    """
    client = _build_client()

    amount = AuthAmount(order_amount=10000, price_currency="USD")  # 100.00 USD = 10000 cents
    request = AuthRequest(
        app_id=TEST_APP_ID,
        merchant_id=TEST_MERCHANT_ID,
        reference_order_id=f"ORDER_AUTH_{int(time.time() * 1000)}",
        transaction_request_id=f"AUTH_REQ_{int(time.time() * 1000)}",
        amount=amount,
        description="Integration test auth",
        terminal_sn=TEST_TERMINAL_SN,
        attach='{"test":"auth"}',
        notify_url="https://merchant.com/notify",
        time_expire=_iso8601_after_minutes(10),
    )

    try:
        response = client.auth(request)
        assert response is not None

        test_logger.info(
            "Auth integration parsed by SDK - code=%s, msg=%s, trace_id=%s, "
            "transaction_id=%s, transaction_request_id=%s",
            getattr(response, "code", None),
            getattr(response, "msg", None),
            getattr(response, "trace_id", None),
            getattr(response, "transaction_id", None),
            getattr(response, "transaction_request_id", None),
        )
    except SunbayNetworkError as e:
        pytest.fail(f"Network error during auth integration test: {e}")
    except SunbayBusinessError as e:
        test_logger.info("Auth integration business error (expected): code=%s, msg=%s", e.code, e)


def test_forced_auth_integration():
    """
    真正调用 forced_auth 接口的集成测试，用于验证 NexusClient.forced_auth 整条链路。
    """
    client = _build_client()

    amount = AuthAmount(order_amount=10000, price_currency="USD")
    request = ForcedAuthRequest(
        app_id=TEST_APP_ID,
        merchant_id=TEST_MERCHANT_ID,
        reference_order_id=f"ORDER_FORCED_AUTH_{int(time.time() * 1000)}",
        transaction_request_id=f"FORCED_AUTH_REQ_{int(time.time() * 1000)}",
        amount=amount,
        description="Integration test forced auth",
        terminal_sn=TEST_TERMINAL_SN,
        attach='{"test":"forced_auth"}',
        notify_url="https://merchant.com/notify",
        time_expire=_iso8601_after_minutes(10),
    )

    try:
        response = client.forced_auth(request)
        assert response is not None

        test_logger.info(
            "ForcedAuth integration parsed by SDK - code=%s, msg=%s, trace_id=%s, "
            "transaction_id=%s, transaction_request_id=%s",
            getattr(response, "code", None),
            getattr(response, "msg", None),
            getattr(response, "trace_id", None),
            getattr(response, "transaction_id", None),
            getattr(response, "transaction_request_id", None),
        )
    except SunbayNetworkError as e:
        pytest.fail(f"Network error during forced_auth integration test: {e}")
    except SunbayBusinessError as e:
        test_logger.info("ForcedAuth integration business error (expected): code=%s, msg=%s", e.code, e)


def test_incremental_auth_integration():
    """
    真正调用 incremental_auth 接口的集成测试，用于验证 NexusClient.incremental_auth 整条链路。
    """
    client = _build_client()

    amount = AuthAmount(order_amount=5000, price_currency="USD")  # 50.00 USD = 5000 cents
    request = IncrementalAuthRequest(
        app_id=TEST_APP_ID,
        merchant_id=TEST_MERCHANT_ID,
        original_transaction_request_id=EXISTING_TRANSACTION_REQUEST_ID,
        transaction_request_id=f"INCREMENTAL_AUTH_REQ_{int(time.time() * 1000)}",
        amount=amount,
        description="Integration test incremental auth",
        terminal_sn=TEST_TERMINAL_SN,
        attach='{"test":"incremental_auth"}',
        notify_url="https://merchant.com/notify",
    )

    try:
        response = client.incremental_auth(request)
        assert response is not None

        test_logger.info(
            "IncrementalAuth integration parsed by SDK - code=%s, msg=%s, trace_id=%s, "
            "transaction_id=%s, transaction_request_id=%s",
            getattr(response, "code", None),
            getattr(response, "msg", None),
            getattr(response, "trace_id", None),
            getattr(response, "transaction_id", None),
            getattr(response, "transaction_request_id", None),
        )
    except SunbayNetworkError as e:
        pytest.fail(f"Network error during incremental_auth integration test: {e}")
    except SunbayBusinessError as e:
        test_logger.info("IncrementalAuth integration business error (expected): code=%s, msg=%s", e.code, e)


def test_post_auth_integration():
    """
    真正调用 post_auth 接口的集成测试，用于验证 NexusClient.post_auth 整条链路。
    """
    client = _build_client()

    amount = PostAuthAmount(order_amount=5000, price_currency="USD", tip_amount=1000)  # 50.00 USD + 10.00 tip
    request = PostAuthRequest(
        app_id=TEST_APP_ID,
        merchant_id=TEST_MERCHANT_ID,
        original_transaction_request_id=EXISTING_TRANSACTION_REQUEST_ID,
        transaction_request_id=f"POST_AUTH_REQ_{int(time.time() * 1000)}",
        amount=amount,
        description="Integration test post auth",
        terminal_sn=TEST_TERMINAL_SN,
        attach='{"test":"post_auth"}',
        notify_url="https://merchant.com/notify",
    )

    try:
        response = client.post_auth(request)
        assert response is not None

        test_logger.info(
            "PostAuth integration parsed by SDK - code=%s, msg=%s, trace_id=%s, "
            "transaction_id=%s, transaction_request_id=%s",
            getattr(response, "code", None),
            getattr(response, "msg", None),
            getattr(response, "trace_id", None),
            getattr(response, "transaction_id", None),
            getattr(response, "transaction_request_id", None),
        )
    except SunbayNetworkError as e:
        pytest.fail(f"Network error during post_auth integration test: {e}")
    except SunbayBusinessError as e:
        test_logger.info("PostAuth integration business error (expected): code=%s, msg=%s", e.code, e)


def test_refund_integration():
    """
    真正调用 refund 接口的集成测试，用于验证 NexusClient.refund 整条链路。
    """
    client = _build_client()

    amount = RefundAmount(order_amount=10000, price_currency="USD")  # 100.00 USD = 10000 cents
    request = RefundRequest(
        app_id=TEST_APP_ID,
        merchant_id=TEST_MERCHANT_ID,
        transaction_request_id=f"REFUND_REQ_{int(time.time() * 1000)}",
        amount=amount,
        original_transaction_request_id=EXISTING_TRANSACTION_REQUEST_ID,
        description="Integration test refund",
        terminal_sn=TEST_TERMINAL_SN,
        attach='{"test":"refund"}',
        notify_url="https://merchant.com/notify",
        time_expire=_iso8601_after_minutes(10),
    )

    try:
        response = client.refund(request)
        assert response is not None

        test_logger.info(
            "Refund integration parsed by SDK - code=%s, msg=%s, trace_id=%s, "
            "transaction_id=%s, transaction_request_id=%s, original_transaction_id=%s",
            getattr(response, "code", None),
            getattr(response, "msg", None),
            getattr(response, "trace_id", None),
            getattr(response, "transaction_id", None),
            getattr(response, "transaction_request_id", None),
            getattr(response, "original_transaction_id", None),
        )
    except SunbayNetworkError as e:
        pytest.fail(f"Network error during refund integration test: {e}")
    except SunbayBusinessError as e:
        test_logger.info("Refund integration business error (expected): code=%s, msg=%s", e.code, e)


def test_void_integration():
    """
    真正调用 void_transaction 接口的集成测试，用于验证 NexusClient.void_transaction 整条链路。
    """
    client = _build_client()

    request = VoidRequest(
        app_id=TEST_APP_ID,
        merchant_id=TEST_MERCHANT_ID,
        transaction_request_id=f"VOID_REQ_{int(time.time() * 1000)}",
        original_transaction_request_id=EXISTING_TRANSACTION_REQUEST_ID,
        description="Integration test void",
        terminal_sn=TEST_TERMINAL_SN,
        attach='{"test":"void"}',
        notify_url="https://merchant.com/notify",
    )

    try:
        response = client.void_transaction(request)
        assert response is not None

        test_logger.info(
            "Void integration parsed by SDK - code=%s, msg=%s, trace_id=%s, "
            "original_transaction_id=%s, original_transaction_request_id=%s",
            getattr(response, "code", None),
            getattr(response, "msg", None),
            getattr(response, "trace_id", None),
            getattr(response, "original_transaction_id", None),
            getattr(response, "original_transaction_request_id", None),
        )
    except SunbayNetworkError as e:
        pytest.fail(f"Network error during void integration test: {e}")
    except SunbayBusinessError as e:
        test_logger.info("Void integration business error (expected): code=%s, msg=%s", e.code, e)


def test_tip_adjust_integration():
    """
    真正调用 tip_adjust 接口的集成测试，用于验证 NexusClient.tip_adjust 整条链路。
    """
    client = _build_client()

    request = TipAdjustRequest(
        app_id=TEST_APP_ID,
        merchant_id=TEST_MERCHANT_ID,
        terminal_sn=TEST_TERMINAL_SN,
        original_transaction_request_id=EXISTING_TRANSACTION_REQUEST_ID,
        tip_amount=2000,  # 20.00 USD = 2000 cents
        attach='{"test":"tip_adjust"}',
    )

    try:
        response = client.tip_adjust(request)
        assert response is not None

        test_logger.info(
            "TipAdjust integration parsed by SDK - code=%s, msg=%s, trace_id=%s, "
            "tip_amount=%s",
            getattr(response, "code", None),
            getattr(response, "msg", None),
            getattr(response, "trace_id", None),
            getattr(response, "tip_amount", None),
        )
    except SunbayNetworkError as e:
        pytest.fail(f"Network error during tip_adjust integration test: {e}")
    except SunbayBusinessError as e:
        test_logger.info("TipAdjust integration business error (expected): code=%s, msg=%s", e.code, e)


def test_batch_query_integration():
    """
    真正调用 batch_query 接口的集成测试，用于验证 NexusClient.batch_query 整条链路。
    """
    client = _build_client()

    request = BatchQueryRequest(
        app_id=TEST_APP_ID,
        merchant_id=TEST_MERCHANT_ID,
        terminal_sn=TEST_TERMINAL_SN,
    )

    try:
        response = client.batch_query(request)
        assert response is not None

        test_logger.info(
            "BatchQuery integration parsed by SDK - code=%s, msg=%s, trace_id=%s, "
            "batch_list count=%s",
            getattr(response, "code", None),
            getattr(response, "msg", None),
            getattr(response, "trace_id", None),
            len(response.batch_list) if response.batch_list else 0,
        )
        if response.batch_list:
            for idx, batch_item in enumerate(response.batch_list[:3]):  # Log first 3 items
                test_logger.info(
                    "BatchQuery item[%d] - batch_no=%s, channel_code=%s, price_currency=%s, "
                    "total_count=%s, net_amount=%s",
                    idx,
                    getattr(batch_item, "batch_no", None),
                    getattr(batch_item, "channel_code", None),
                    getattr(batch_item, "price_currency", None),
                    getattr(batch_item, "total_count", None),
                    getattr(batch_item, "net_amount", None),
                )
    except SunbayNetworkError as e:
        pytest.fail(f"Network error during batch_query integration test: {e}")
    except SunbayBusinessError as e:
        test_logger.info("BatchQuery integration business error (expected): code=%s, msg=%s", e.code, e)


def test_batch_close_integration():
    """
    真正调用 batch_close 接口的集成测试，用于验证 NexusClient.batch_close 整条链路。
    """
    client = _build_client()

    request = BatchCloseRequest(
        app_id=TEST_APP_ID,
        merchant_id=TEST_MERCHANT_ID,
        transaction_request_id=f"BATCH_CLOSE_REQ_{int(time.time() * 1000)}",
        terminal_sn=TEST_TERMINAL_SN,
        channel_code=None,
        description="Integration test batch close",
    )

    try:
        response = client.batch_close(request)
        assert response is not None

        test_logger.info(
            "BatchClose integration parsed by SDK - code=%s, msg=%s, trace_id=%s, "
            "batch_no=%s, terminal_sn=%s, batch_time=%s, transaction_count=%s, "
            "price_currency=%s, net_amount=%s",
            getattr(response, "code", None),
            getattr(response, "msg", None),
            getattr(response, "trace_id", None),
            getattr(response, "batch_no", None),
            getattr(response, "terminal_sn", None),
            getattr(response, "batch_time", None),
            getattr(response, "transaction_count", None),
            getattr(response, "price_currency", None),
            getattr(response, "net_amount", None),
        )
    except SunbayNetworkError as e:
        pytest.fail(f"Network error during batch_close integration test: {e}")
    except SunbayBusinessError as e:
        test_logger.info("BatchClose integration business error (expected): code=%s, msg=%s", e.code, e)


