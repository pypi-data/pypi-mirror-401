"""
User models for Velt SDK

Based on Velt API documentation:
https://docs.velt.dev/api-reference/sdk/models/data-models
"""
from typing import Optional, Dict, Any, List
from dataclasses import dataclass



@dataclass
class PartialUser:
    """
    Partial user model
    
    Based on: https://docs.velt.dev/api-reference/sdk/models/data-models#partialuser
    """
    userId: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'userId': self.userId
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PartialUser':
        """Create from dictionary"""
        return cls(
            userId=data.get('userId', '')
        )


@dataclass
class PartialTaggedUserContacts:
    """
    Partial tagged user contacts model
    
    Based on: https://docs.velt.dev/api-reference/sdk/models/data-models#partialtaggedusercontacts
    """
    userId: str
    contact: Optional['PartialUser'] = None
    text: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result: Dict[str, Any] = {
            'userId': self.userId
        }
        if self.contact is not None:
            result['contact'] = self.contact.to_dict() if isinstance(self.contact, PartialUser) else self.contact
        if self.text is not None:
            result['text'] = self.text
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PartialTaggedUserContacts':
        """Create from dictionary"""
        contact = None
        if 'contact' in data and data['contact']:
            if isinstance(data['contact'], dict):
                contact = PartialUser.from_dict(data['contact'])
            elif isinstance(data['contact'], PartialUser):
                contact = data['contact']
        
        return cls(
            userId=data.get('userId', ''),
            contact=contact,
            text=data.get('text')
        )


@dataclass
class User:
    """
    User model for GetUserResolver response
    
    Based on: https://docs.velt.dev/api-reference/sdk/models/data-models#user
    """
    userId: str
    name: Optional[str] = None
    photoUrl: Optional[str] = None
    email: Optional[str] = None
    color: Optional[str] = None
    textColor: Optional[str] = None
    initial: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result: Dict[str, Any] = {
            'userId': self.userId
        }
        if self.name is not None:
            result['name'] = self.name
        if self.photoUrl is not None:
            result['photoUrl'] = self.photoUrl
        if self.email is not None:
            result['email'] = self.email
        if self.color is not None:
            result['color'] = self.color
        if self.textColor is not None:
            result['textColor'] = self.textColor
        if self.initial is not None:
            result['initial'] = self.initial
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create from dictionary"""
        return cls(
            userId=data.get('userId', ''),
            name=data.get('name'),
            photoUrl=data.get('photoUrl'),
            email=data.get('email'),
            color=data.get('color'),
            textColor=data.get('textColor'),
            initial=data.get('initial')
        )


@dataclass
class GetUserResolverRequest:
    """
    Request model for GetUserResolver endpoint
    
    Based on: https://docs.velt.dev/api-reference/sdk/models/data-models#getuserresolverrequest
    """
    organizationId: str
    userIds: List[str]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GetUserResolverRequest':
        """
        Create GetUserResolverRequest from dictionary
        
        Args:
            data: Dictionary containing request fields
            
        Returns:
            GetUserResolverRequest instance
        """
        return cls(
            organizationId=data.get('organizationId', ''),
            userIds=data.get('userIds', [])
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'organizationId': self.organizationId,
            'userIds': self.userIds
        }
