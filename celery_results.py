from celery_tasks import add
import time

result = add.apply_async(
    args=[5,5]
)

time.sleep(10)

if result.ready():
    print('Task result: ', result.get(timeout=1))

print(result.state)
print(result.id)
print(result.backend)
