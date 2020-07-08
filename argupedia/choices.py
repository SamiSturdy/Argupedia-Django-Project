from django.db import models
from django.utils.translation import gettext_lazy as _

class ActionCQChoices(models.TextChoices):
    IS_S_TRUE = 'IsSTrue', _('Is the situation, S, true?')
    DOES_A_ACHIEVE_G = 'DoesAAchieveG', _('Does the action, A, achieve the goal, G?')
    ALTERNATIVE_A_ACHIEVES_G = 'AlternativeAAchievesG', _('Is there an alternative action, A\' that achieves the goal, G?')

class ExpertCQChoices(models.TextChoices):
    E_CREDIBLE = 'ECredible', _('Is the expert, E, credible as an expert?')
    D_RELEVANT_TO_A = 'DRelevantToA', _('Is the domain, D, of the expert relevant to the assertion, A?')
    DOES_ASSERTION_IMPLY_A = 'DoesAssertionImplyA', _('Does the actual assertion of the expert, E, truly imply the given assertion, A?')
    E_RELIABLE = 'EReliable', ('Is the expert, E, reliable?')
    A_CONSISTENT = 'AConsistent', ('Is the assertion, A, consistent with other experts\' assertions?')
    A_BASED_ON_EVIDENCE = 'IsABasedOnEvidence', ('Is the assertion, A, based on evidence?')

class PopularCQChoices(models.TextChoices):
    EVIDENCE_A_ACCEPTED = 'EvidenceAAccepted', _('Is there evidence that suggests the assertion, A, is generally accepted?')
    BELIEF_ACCURATE = 'BeliefAccurate', _('Even if the assertion, A, is generally accepted to be true, is there a reason to believe it is inaccurate?')
