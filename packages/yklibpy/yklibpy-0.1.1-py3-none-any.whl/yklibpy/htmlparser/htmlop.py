from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import Optional

class HtmlOp:
	class Tagx:
		def __init__(self, tag: Tag, namex: str):
			self.tag = tag
			self.strx = str(tag)
			self.type = type(tag)
			self.mes_type = f"  type({namex}): { str(type(namex)) }"
			if hasattr(tag, 'get_text'):
				self.text = tag.get_text(strip=True)
				self.mes_text = f"  {namex}_text: {self.text}"
			else:
				self.mes_text = f"  {namex}_text: [Nothing]"

			if hasattr(tag, 'name'):
				self.mes_name = f"  {namex}.name: { tag.name }"
				# print()
			else:
				self.mes_name = f"  {namex}.name: [Nothing]"
		def set_option(self, option):
			self.option = option
		def get_option(self):
			return self.option

	class AnchorTagx(Tagx):
		def __init__(self, anchor_tag):
			super().__init__(anchor_tag, "anchor")
			self.href = self.tag.get("href", "")
			self.text = self.tag.get_text(strip=True)
			self.mes_href = f"  href: {self.href}"
			self.mes_text = f"  text: {self.text}"
		def show(self):
			return "\n".join([self.href, self.text])

	class AnchorTagInfo:
		def __init__(self, anchor_tag):
			self.anchor = HtmlOp.AnchorTagx(anchor_tag)

		def setup(self):
			# print()
			self.next_sibling = Tagx(self.anchor.tag.next_sibling, "next_sibling")
			self.parent = Tagx(self.anchor.tag.next_sibling, "parent")
			self.parent_parent = Tagx(self.anchor.tag.parent.parent, "parent.parent")

	class PriceInfo:
		def __init__(self, price_old, price_real):
			self.price_old = price_old
			self.price_real = price_real
		def get_price_old(self):
			if self.price_old is None:
				return None
			return self.price_old.get_option()
		def get_price_real(self):
			if self.price_real is None:
				return None
			return self.price_real.get_option()

	@classmethod
	def get_anchor_under_b(cls, child, cond = None):
		if cond is None:
			list = child.find_all("b")
		else:
			list = child.find_all("b", cond)
		assoc_array = [ cls.get_anchor_all(b_tag) for b_tag in list ]

		return assoc_array

	@classmethod
	def get_anchor_all(cls, child):
		return [cls.get_anchor_tag_info(anchor_tag) for anchor_tag in child.find_all("a")]

	@classmethod
	def get_anchor_tag_info(cls, anchor_tag):
		if anchor_tag is None:
			return None

		# print('----')
		a_tag_info = cls.AnchorTagInfo(anchor_tag)

		return a_tag_info

	@classmethod
	def get_anchor_under_div(cls, child, cond = None):
		if cond is None:
			list = child.find_all("div", cond)
		else:
			list = child.find_all("div")

		for div_tag in list:
			print(f"get_anchor_under_div div_tag: {div_tag}")
			anchor_tag_info_array = HtmlOp.get_anchor_all(div_tag)
			for anchor_tag_info in anchor_tag_info_array:
				cls.print_tag_info(anchor_tag_info)

	'''
	@classmethod
	def print_tag_info(cls, assoc):
		tag = assoc["tag"]
		print(tag)

		mes_array = assoc["mes_array"]
		mes = "\n".join(mes_array)
		print(mes)
	'''
