from django.db import connection
from django.test import override_settings
from saas_base.test import SaasTestCase
from tests.demo_app.models import UserSecret


class TestUserSecrets(SaasTestCase):
    user_id = SaasTestCase.GUEST_USER_ID

    def get_db_value(self, field: str, model_id: int):
        cursor = connection.cursor()
        cursor.execute(
            f"select {field} from demo_app_usersecret where id = {model_id};"
        )
        return cursor.fetchone()[0]

    def test_create_user_secrets(self):
        obj = UserSecret(secret_key=b'test')
        obj.save()
        self.assertEqual(obj.secret_key, b'test')

        db_value = self.get_db_value('secret_key', obj.pk)
        self.assertEqual(len(db_value.split('.')), 5)

    def test_key_fallback(self):
        obj = UserSecret(secret_key=b'test')
        obj.save()
        self.assertEqual(obj.secret_key, b'test')

        with override_settings(SECRET_KEY='new-primary-key'):
            new_obj = UserSecret.objects.get(pk=obj.pk)
            # we cannot decreypt it
            self.assertIsNone(new_obj.secret_key)

        with override_settings(SECRET_KEY='new-primary-key', SECRET_KEY_FALLBACKS=['django-insecure']):
            fallback_obj = UserSecret.objects.get(pk=obj.pk)
            self.assertEqual(fallback_obj.secret_key, b'test')
