from app.services.policy.engine import evaluate_action


def test_policy_high_send_blocked():
    out = evaluate_action('email.send')
    assert out['risk_level'] == 'HIGH'
