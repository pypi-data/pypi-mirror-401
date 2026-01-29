
class _ProtobufListWrapper:
	def __init__(self, proto_field, wrapper_class=None):
		self._proto_field = proto_field
		self._wrapper_class = wrapper_class
	def __getitem__(self, index):
		if self._wrapper_class:
			return self._wrapper_class(proto_message=self._proto_field[index])
		else:
			return self._proto_field[index]
	def __setitem__(self, index, value):
		if self._wrapper_class and hasattr(value, 'to_proto'):
			self._proto_field[index].CopyFrom(value.to_proto())
		else:
			self._proto_field[index] = value
	def __delitem__(self, index):
		del self._proto_field[index]
	def __len__(self):
		return len(self._proto_field)
	def __iter__(self):
		for i in range(len(self._proto_field)):
			yield self[i]
	def append(self, value):
		if self._wrapper_class and hasattr(value, 'to_proto'):
			new_item = self._proto_field.add()
			new_item.CopyFrom(value.to_proto())
		else:
			self._proto_field.append(value)
	def extend(self, values):
		for value in values:
			self.append(value)
	def insert(self, index, value):
		if self._wrapper_class and hasattr(value, 'to_proto'):
			new_item = self._proto_field.add()
			new_item.CopyFrom(value.to_proto())
			for i in range(len(self._proto_field) - 1, index, -1):
				self._proto_field[i].CopyFrom(self._proto_field[i - 1])
			self._proto_field[index].CopyFrom(new_item)
		else:
			self._proto_field.insert(index, value)
	def remove(self, value):
		if self._wrapper_class and hasattr(value, 'to_proto'):
			for i in range(len(self._proto_field)):
				if self._proto_field[i] == value.to_proto():
					del self._proto_field[i]
					return
		else:
			self._proto_field.remove(value)
	def clear(self):
		self._proto_field.clear()
	def __str__(self):
		return str(list(self))
	def __repr__(self):
		return repr(list(self))

class _ProtobufMapWrapper:
	def __init__(self, proto_field):
		self._proto_field = proto_field
	def __getitem__(self, key):
		return self._proto_field[key]
	def __setitem__(self, key, value):
		self._proto_field[key] = value
	def __delitem__(self, key):
		del self._proto_field[key]
	def __len__(self):
		return len(self._proto_field)
	def __iter__(self):
		return iter(self._proto_field)
	def __contains__(self, key):
		return key in self._proto_field
	def keys(self):
		return self._proto_field.keys()
	def values(self):
		return self._proto_field.values()
	def items(self):
		return self._proto_field.items()
	def get(self, key, default=None):
		return self._proto_field.get(key, default)
	def update(self, other):
		if hasattr(other, 'items'):
			for key, value in other.items():
				self._proto_field[key] = value
		else:
			for key, value in other:
				self._proto_field[key] = value
	def clear(self):
		self._proto_field.clear()
	def pop(self, key, default=None):
		if key in self._proto_field:
			value = self._proto_field[key]
			del self._proto_field[key]
			return value
		return default
	def popitem(self):
		if not self._proto_field:
			raise KeyError('popitem(): dictionary is empty')
		key = next(iter(self._proto_field))
		value = self._proto_field[key]
		del self._proto_field[key]
		return key, value
	def setdefault(self, key, default=None):
		if key not in self._proto_field:
			self._proto_field[key] = default
		return self._proto_field[key]
	def __str__(self):
		return str(dict(self._proto_field))
	def __repr__(self):
		return repr(dict(self._proto_field))
