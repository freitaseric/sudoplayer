class EmbedAuthor:
    def __init__(self, name: str, icon_url: str | None = None, url: str | None = None):
        self.name = name
        self.icon_url = icon_url
        self.url = url

    def to_dict(self):
        return {"name": self.name, "icon_url": self.icon_url, "url": self.url}


class EmbedFooter:
    def __init__(self, text: str, icon_url: str | None = None):
        self.text = text
        self.icon_url = icon_url

    def to_dict(self):
        return {"text": self.text, "icon_url": self.icon_url}


class EmbedField:
    def __init__(self, name: str, value: str, inline: bool = False):
        self.name = name
        self.value = value
        self.inline = inline

    def to_dict(self):
        return {"name": self.name, "value": self.value, "inline": self.inline}
