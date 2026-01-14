# Events

## Intro

This component provides a flexible event-driven architecture for building scalable, reliable, and maintainable applications.

## Defining Events

An event is quite simply just a data object which holds the information related to the event. An event does not contain any logic.

```python
from neva.events import Event

class UserCreated(Event):
    user_id: int
    email: str

class UserNotificationRequested(Event):
    user_id: int
    message: str

class OrderFulfillmentRequested(Event):
    order_id: int
    items: list[dict]
    total_amount: float
```

Under the hood, the  `Event` class is a Pydantic model and thus can leverage all Pydantic features:

```python
from pydantic import Field, field_validator
from datetime import datetime

class OrderPlaced(Event):
    order_id: int
    user_id: int
    amount: float = Field(gt=0, description="Order amount in dollars")
    placed_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if v > 100000:
            raise ValueError('Order amount exceeds maximum')
        return v
```

## Defining listeners

Listeners are classes that implement the `Listener` Protocol. This Protocol simply defines the signature of the `handle` method that listeners must implement.

```python
from neva import Result, Ok, Err

class SendWelcomeEmailListener:
    async def handle(self, event: UserCreated) -> Result[None, str]:
        result = await self.email_service.send_welcome(event.email)
        return result.map(lambda _: None)
```

## Registering events and listeners

Listeners can be registered using the `listen` method of the `Event` facade within the `lifespan` method of a `ServiceProvider`.

```python
from contextlib import asynccontextmanager

from neva import Ok, Result
from neva.arch import ServiceProvider
from neva.events import Event

class EventServiceProvider(ServiceProvider):
    @asynccontextmanager
    async def lifespan(self) -> AsyncIterator[None]:
        Event.listen(UserCreated, ValidateUserQuotaListener)
        Event.listen(UserCreated, SendWelcomeEmailListener)
        Event.listen(UserCreated, CreateUserProfileListener)

        Event.listen(OrderPlaced, SendOrderConfirmationListener)
        Event.listen(OrderPlaced, UpdateInventoryListener)
        Event.listen(OrderPlaced, NotifyWarehouseListener)

        return Ok(self)
```

## Listener execution policy

By default, listeners are executed as soon as the subscribed event is dispatched and executed synchronously. This may not be the behavior you need, so we provide a few ways to control this.

There are three different execution policies:

- `IMMEDIATE`: The default behaviour. The listener is executed immediately and synchronously, regardless of the transaction status.
- `DEFERRED`: The listener is executed synchronously after the transaction successfully commits. If no transaction is active, behaves just like the `IMMEDIATE` policy.
- `OUTBOX`: An extension of the `DEFERRED` policy. If any outboxed listeners subscribes to an event, this event is saved to an outbox queue once the transaction successfully commits. A background process will then pick up then event and enqueue the appropriate listeners to be executed as background tasks.

The `OUTBOX` policy is particularly useful for long-running tasks that need to be executed in the background, but requires significant setup before being used.

### Specifying policy in listener definition

To specify the policy of a listener, you may define a `policy` parameter when defining the listener class. If no such parameter is defined, the listener defers to the `IMMEDIATE` policy.

```python
class TestListener:
    policy: ListenerPolicy = "deferred"
    ...
```

```python
class TestListener:
    policy: ListenerPolicy = "outbox"
    ...
```

### Specifying policy in event registration

Alternatively, you may specify the policy when registering an event listener:

```python
class EventServiceProvider(ServiceProvider):
    @asynccontextmanager
    async def lifespan(self) -> AsyncIterator[None]:
        Event.listen(UserCreated, ValidateUserQuotaListener, policy="deferred")
```

If any `policy` attribute is defined on the listener class, it will be overwritten by the one specified when registering the listener.

## Handling Failure

The consequence of a failure depend entirely on the policy of the listener. As such you should be extremely mindful of these consequences when writing your listeners and choosing their policy.

When dispatching an event using the default `dispatch` on the model or the `Event` facade, any immediate listeners that returns an error will immediately stop the event processing and immediately raise an exception. While this may seem to break the flow of the application, in this particular case this helps to ensure that the transaction is rolled back and the error is propagated to the calling code and particularly to any context manager, specifically the current transaction.

For `DEFERRED` listeners, the `dispatch` method returns an `DispatchTracker`. This object lets you inspect the result of `DEFERRED` listeners for the given event. This is useful for proactive error handling, for example if failure of an event should lead to return a specific HTTP response code to the caller.

For `OUTBOX` listeners, you may define a failure callback on the listener class. This will be called if the event fails for any reason (non-recoverable error, exhausted retry policy...). Usually for outbox listeners you want to log the error or notify some operational team. Anything more than that should probably not be handled by an event system to begin with.

## Testing

The `Event` facade exposes testing utilities to prevent actual listener execution and make assertions about dispatched events:

```python
from neva.events import Event

def test_user_creation_dispatches_event():
    # Prevent actual listener execution
    Event.fake()

    # Perform action that dispatches events
    user = create_user(email="test@example.com")

    # Assert events were dispatched
    Event.assertDispatched(UserCreated, lambda e: e.email == "test@example.com")
    Event.assertDispatched(UserNotificationRequested)

    # Assert events were NOT dispatched
    Event.assertNotDispatched(UserDeleted)

def test_user_creation_with_specific_listener():
    # Fake all except specific listeners
    Event.fake([ValidateUserQuotaListener])

    # This listener will actually run, others won't
    user = create_user(email="test@example.com")
```

Testing utilities use the existing mocking infrastructure (flexmock or similar) to intercept event dispatching while maintaining type safety and Result semantics.

## Ideas

Other ideas not yet specified:

- Decorator to define listeners as pure functions
- Priority system for listeners ordering
- Critical flag for deferred listeners
- `Auditable` flag for events
