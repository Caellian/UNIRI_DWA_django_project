View `request` user:
```python
if request.user.is_authenticated:
    pass # Do something for authenticated users.
else:
    pass # Do something for anonymous users.
```