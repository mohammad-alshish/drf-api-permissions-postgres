from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Game


# Create your tests here.
class GameTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        testuser2 = get_user_model().objects.create_user(
            username="testuser2", password="pass"
        )
        testuser1.save()

        test_game = Game.objects.create(
            game_name="mmm",
            owner=testuser1,
            description="wow",
        )
        test_game.save()

    def setUp(self):
        self.client.login(username='testuser1', password="pass")

    def test_things_model(self):
        game = Game.objects.get(id=1)
        actual_owner = str(game.owner)
        actual_name = str(game.game_name)
        actual_description = str(game.description)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_name, "mmm")
        self.assertEqual(
            actual_description, "wow"
        )

    def test_get_thing_list(self):
        url = reverse("game_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        games = response.data
        self.assertEqual(len(games), 1)
        self.assertEqual(games[0]["game_name"], "mmm")

    def test_auth_required(self):
        self.client.logout()
        url = reverse("game_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_owner_can_delete(self):
        self.client.logout()
        self.client.login(username='testuser2', password="pass")
        url = reverse("game_detail", args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
