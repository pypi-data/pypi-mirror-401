from typing import Any, Callable
from weakref import WeakKeyDictionary


class NexusField:
    def __init__(self, key: str, default: Any = None):
        self.key = key
        self.default = default
        self._instance_callbacks: WeakKeyDictionary = WeakKeyDictionary()
    
    def __get__(self, instance, owner):
        if instance is None: return self
        return instance.value(self.key, default=self.default)
    
    def __set__(self, instance, value):
        if instance is None: return
        was_changed = instance.setValue(self.key, value)
        
        if was_changed and not instance._signals_blocked:
            self._notify(instance, value)
    
    def _notify(self, instance, value):
        callbacks = self._instance_callbacks.get(instance, [])
        for cb in callbacks:
            cb(value)
    
    def connect(self, instance, callback: Callable):
        if instance not in self._instance_callbacks:
            self._instance_callbacks[instance] = []
        self._instance_callbacks[instance].append(callback)
