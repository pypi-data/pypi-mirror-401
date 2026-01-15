from enum import Enum
from typing import List, Optional

from looqbox.integration.integration_links import user_login as get_user_login
from looqbox.integration.user import User
from looqbox.objects.component_utility.css_option import CssOption
from looqbox.objects.looq_object import LooqObject
from looqbox.render.abstract_render import BaseRender


class AvatarSourceType(Enum):
    LOGIN = "login"
    ID = "id"
    LINK = "link"


class ObjAvatar(LooqObject):
    """
    Renders a user's avatar image inside a response.
    """

    alt: str = None
    gap: int = None
    # Temporally removed. It must be confirmed with the Frontend when it will be implemented
    # icon: ObjIcon = None icon (ObjIcon, optional): Custom icon used alongside the user's avatar
    shape_options: List[str] = ["circle", "square"]  # options available for the Ant Design
    shape: str = None
    source: int | str = None
    source_avatar_image: dict = {}
    source_type: AvatarSourceType = AvatarSourceType.LOGIN

    def __init__(self, source: int | str = None,
                 alt: str = None,
                 gap: int = None,
                 shape: str = "circle",
                 source_type: AvatarSourceType | str = AvatarSourceType.LOGIN,
                 css_options: Optional[List[CssOption]] = None,
                 tab_label: str = None):

        """
        Args:
            source (str|int, optional): Parameter passed to the backend to search for the user image.
            alt (str, optional): This attribute defines the alternative text describing the image.
            gap (Int, optional): Letter type unit distance between left and right sides.
            shape (str, optional): The shape of avatar image (can be set as circle or square).
            source_type(AvatarQueryMethod|str, optional): Method used to search for the avatar image (can be set to use login or id)
            tab_label (str, optional): Set the name of the tab in the frame.
            css_options (list, optional): set the correspond css property.

        Examples:
            >>> avatar = ObjAvatar(source_type = "login")
            >>> avatar.set_user_login("MyLogin")
            >>> # or using id
            >>> avatar.set_user_id(10, source_type = "id")
        """

        super().__init__(css_options=css_options, tab_label=tab_label)

        self.source = source
        self.alt = alt
        self.gap = gap
        self.shape = shape if shape in self.shape_options else "circle"
        self._set_source_type(source_type)

    def from_user(self, usr: User):
        self.set_user_login(usr.login)

    def set_user_id(self, user_id: int) -> None:
        self.source = user_id
        self._set_source_type(AvatarSourceType.ID)

    def set_user_login(self, user_login: str) -> None:
        self.source = user_login
        self._set_source_type(AvatarSourceType.LOGIN)

    def set_source_link(self, link: str) -> None:
        self.source = link
        self._set_source_type(AvatarSourceType.LINK)

    def set_user(self, login: str = None, id: int = None) -> None:
        if login:
            self.set_user_login(login)
        elif id:
            self.set_user_id(id)
        else:
            raise ValueError("You must provide a login or id")

    def build_self_avatar(self) -> None:
        """
        Build the ObjAvatar based on the user who calls the class
        """
        self.source = get_user_login()
        self._set_source_type(type=AvatarSourceType.LOGIN)

    def to_json_structure(self, visitor: BaseRender):
        self._set_image_source()
        return visitor.avatar_render(self)

    def _set_image_source(self):

        src_options = {
            AvatarSourceType.LOGIN: lambda: {"type": "userLogin", "content": self.source},
            AvatarSourceType.ID: lambda: {"type": "userId", "content": self.source},
            AvatarSourceType.LINK: lambda: {"type": "link", "content": self.source}
        }

        self.source_avatar_image = src_options[self.source_type]()
        if self._is_avatar_source_not_set():
            raise Exception("The avatar source reference is not set")

    def _is_avatar_source_not_set(self):
        return None in self.source_avatar_image.values()

    def _set_source_type(self, type: str | AvatarSourceType):
        if isinstance(type, AvatarSourceType):
            self.source_type = type
        else:
            try:
                self.source_type = AvatarSourceType[type.upper()]
            except KeyError as key_error:
                raise KeyError(
                    f"Could not use {type} as method, "
                    f"please one use of these instead: "
                    f"{', '.join([available_method.name for available_method in AvatarSourceType])}")
            except Exception as e:
                raise e

    def __eq__(self, other):
        return self.source == other.source and self.shape == other.shape

    def __str__(self):
        return f"method: {self.source_type.name}\nvalue: {self.source}\nshape: {self.shape}"
