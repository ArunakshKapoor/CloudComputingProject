from app.services.simulation.simulator import preview_for_step


class S:
    action_type='email.draft'


def test_preview_email():
    assert 'Subject' in preview_for_step(S())
