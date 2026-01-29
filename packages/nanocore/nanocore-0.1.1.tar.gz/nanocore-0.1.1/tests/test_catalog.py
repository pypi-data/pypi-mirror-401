"""
Tests for service discovery and catalog functionality.
"""

import pytest
import asyncio
from nanocore.broker import Broker
from nanocore.worker import Worker
from nanocore.rpn_worker import RPNWorker


class TestWorkerIntrospection:
    """Test worker handler introspection."""

    def test_worker_handlers_property(self):
        """Verify that Worker.handlers property returns registered handlers."""
        worker = Worker()

        # Initially empty
        assert worker.handlers == {}

        # Register some handlers
        def handler1(msg):
            pass

        def handler2(msg):
            pass

        worker.register_handler("type1", handler1)
        worker.register_handler("type2", handler2)

        # Check handlers are accessible
        handlers = worker.handlers
        assert "type1" in handlers
        assert "type2" in handlers
        assert handlers["type1"] == handler1
        assert handlers["type2"] == handler2

    def test_rpn_worker_handlers(self):
        """Verify that specialized workers expose their handlers."""
        worker = RPNWorker()

        handlers = worker.handlers
        assert "push" in handlers
        assert "add" in handlers
        assert "sub" in handlers
        assert "mul" in handlers
        assert "div" in handlers
        assert "clear" in handlers


class TestBrokerCatalog:
    """Test broker catalog generation."""

    def test_get_catalog_empty_broker(self):
        """Test catalog with no workers."""
        broker = Broker()
        catalog = broker.get_catalog()

        assert catalog == {"workers": {}, "groups": {}}

    def test_get_catalog_single_worker_no_groups(self):
        """Test catalog with one worker and no groups."""
        broker = Broker()
        worker = RPNWorker()
        broker.register_worker("calc1", worker)

        catalog = broker.get_catalog()

        assert "calc1" in catalog["workers"]
        assert catalog["workers"]["calc1"]["groups"] == []
        assert "push" in catalog["workers"]["calc1"]["handlers"]
        assert "add" in catalog["workers"]["calc1"]["handlers"]

    def test_get_catalog_single_worker_with_group(self):
        """Test catalog with one worker in a group."""
        broker = Broker()
        worker = RPNWorker()
        broker.register_worker("calc1", worker, groups=["math"])

        catalog = broker.get_catalog()

        assert "calc1" in catalog["workers"]
        assert catalog["workers"]["calc1"]["groups"] == ["math"]
        assert "math" in catalog["groups"]
        assert catalog["groups"]["math"] == ["calc1"]

    def test_get_catalog_multiple_workers_multiple_groups(self):
        """Test catalog with complex worker and group configuration."""
        broker = Broker()

        calc1 = RPNWorker()
        calc2 = RPNWorker()
        worker3 = Worker()
        worker3.register_handler("test_handler", lambda x: x)

        broker.register_worker("calc1", calc1, groups=["math", "calculators"])
        broker.register_worker("calc2", calc2, groups=["math"])
        broker.register_worker("worker3", worker3, groups=["utils"])

        catalog = broker.get_catalog()

        # Check workers
        assert len(catalog["workers"]) == 3
        assert "math" in catalog["workers"]["calc1"]["groups"]
        assert "calculators" in catalog["workers"]["calc1"]["groups"]
        assert "math" in catalog["workers"]["calc2"]["groups"]
        assert "utils" in catalog["workers"]["worker3"]["groups"]

        # Check groups
        assert len(catalog["groups"]) == 3
        assert set(catalog["groups"]["math"]) == {"calc1", "calc2"}
        assert catalog["groups"]["calculators"] == ["calc1"]
        assert catalog["groups"]["utils"] == ["worker3"]

        # Check handlers are present
        assert "push" in catalog["workers"]["calc1"]["handlers"]
        assert "test_handler" in catalog["workers"]["worker3"]["handlers"]

    def test_get_catalog_worker_without_handlers(self):
        """Test catalog with worker that has no handlers."""
        broker = Broker()
        worker = Worker()
        broker.register_worker("empty_worker", worker)

        catalog = broker.get_catalog()

        assert "empty_worker" in catalog["workers"]
        assert catalog["workers"]["empty_worker"]["handlers"] == []


@pytest.mark.asyncio
class TestCatalogIntegration:
    """Integration tests for catalog functionality."""

    async def test_catalog_message_flow(self):
        """Test end-to-end catalog request via message."""
        from nanocore.schema import create_message

        broker = Broker()
        worker = RPNWorker()
        broker.register_worker("rpn1", worker, groups=["math"])

        # Simulate catalog request
        catalog = broker.get_catalog()

        # Verify catalog structure
        assert "workers" in catalog
        assert "groups" in catalog
        assert "rpn1" in catalog["workers"]
        assert catalog["workers"]["rpn1"]["groups"] == ["math"]
        assert len(catalog["workers"]["rpn1"]["handlers"]) > 0

    async def test_catalog_response_format(self):
        """Test that catalog can be serialized to JSON."""
        import json
        from nanocore.schema import create_message

        broker = Broker()
        worker = RPNWorker()
        broker.register_worker("rpn1", worker, groups=["math"])

        catalog = broker.get_catalog()

        # Create response message
        response = create_message(
            msg_type="catalog_response",
            body=catalog,
            sender="broker",
            receiver="client",
        )

        # Verify it's JSON serializable
        json_str = json.dumps(response)
        decoded = json.loads(json_str)

        assert decoded["header"]["msg_type"] == "catalog_response"
        assert "workers" in decoded["body"]
        assert "groups" in decoded["body"]
