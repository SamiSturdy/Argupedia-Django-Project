from django.db import models
from polymorphic.models import PolymorphicModel
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Network(models.Model):
    initial_argument = models.ForeignKey('Argument',
                                         on_delete=models.CASCADE,
                                         related_name='initial_argument_network',
                                         null=True)
    date_created = models.DateTimeField(default=timezone.now)

    def grounded_algorithm(self):

        change_detected = True

        arguments = self.argument_set.all()

        while change_detected:

            change_detected = False

            for argument in arguments:
                if not argument.state_check():
                    change_detected = True

class Argument(models.Model):

    class State(models.TextChoices):
        IN = 'in', _('In')
        OUT = 'out', _('Out')
        UNDECIDED = 'undecided', _('Undecided')

    class SchemeType(models.TextChoices):
        ACTION = 'action', _('Action Scheme')
        EXPERT = 'expert', _('Expert Opinion Scheme')
        POPULAR = 'popular', _('Popular Opinion Scheme')

    network = models.ForeignKey('Network', on_delete=models.CASCADE, null=True)
    state = models.CharField(
        max_length=10,
        choices=State.choices,
        default=State.IN
    )
    scheme_type=models.CharField(
        max_length=10,
        choices=SchemeType.choices)
    attacking = models.ForeignKey('self',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True,
                                  related_name='attackers',
                                  related_query_name='attacker')
    target_critical_question = models.CharField(max_length=255, default='Target Critical Question Not Yet Selected')
    date_created = models.DateTimeField(default=timezone.now)

    def state_check(self):
        beginning_state = self.state
        attackers = self.attackers.all()
        if attackers:
            if all(attacker.state == 'out' for attacker in attackers):
                self.state = 'in'
            elif any(attacker.state == 'in' for attacker in attackers):
                self.state = 'out'
            else:
                self.state = 'undecided'
        else:
            self.state = 'in'

        self.save()

        return beginning_state == self.state

class Scheme(PolymorphicModel):
    argument = models.ForeignKey('Argument', on_delete=models.CASCADE, null=True)

class ActionScheme(Scheme):
    situation = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    goal = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

class ExpertOpinionScheme(Scheme):
    domain = models.CharField(max_length=255)
    expert_source = models.CharField(max_length=255)
    assertion = models.CharField(max_length=255)
    reference = models.CharField(max_length=255, blank=True, null=True)

class PopularOpinionScheme(Scheme):
    assertion = models.CharField(max_length=255)
    reference = models.CharField(max_length=255, blank=True, null=True)
