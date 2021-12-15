import pytest

from accounts.models import User


class TestModel:

    def test_create_user(self, db):
        """Test model manager create user method."""
        user = User.objects.create_user(email='normal@user.com', password='foo')
        assert user.email == 'normal@user.com'
        assert user.is_staff == False
        assert user.is_superuser == False
        assert user.is_active == False
        # password is empty
        with pytest.raises(ValueError) as e:
            user1 = User.objects.create_user(email='admin3@gmail.com', password='')
        assert str(e.value) == 'Users must have a password'    
        # email is empty
        with pytest.raises(ValueError) as e:
            user2 = User.objects.create_user(email='', password='admin')
        assert str(e.value) == 'Users must have an email address'
        # email is not given
        with pytest.raises(TypeError) as e:
            user3 = User.objects.create_user(password='admin')
        # email is invalid
        with pytest.raises(ValueError) as e:
            user4 = User.objects.create_user(email='ahmed', password='admin')
        assert str(e.value) == 'You must provide a valid email address.'

    def test_create_superuser(self, db):
        """Test model manager create superuser method."""
        admin_user = User.objects.create_superuser(email='admin2@gmail.com', password='admin1600')
        assert User.objects.filter(is_superuser=True).count() == 1
        assert admin_user.is_staff == True
        assert admin_user.is_superuser == True
        assert admin_user.is_active == True
        assert admin_user.user_type == "A"

    def test_user_str(self, new_user):
        """Test user obj str method."""
        assert new_user.__str__() == 'testemail@gmail.com'

    def test_send_email(self, new_user, mailoutbox):
        """Test send email method."""
        new_user.email_user(subject='subject test', message='message test')
        assert len(mailoutbox) == 1
        mail = mailoutbox[0]
        assert list(mail.to) == [new_user.email]