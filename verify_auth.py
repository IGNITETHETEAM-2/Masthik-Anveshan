"""
Masthik Anveshan - End-to-End Authentication Verification Suite
Tests:
  1. Route protection on / (unauthenticated -> redirect to /login)
  2. Route protection on /pred_page
  3. Login page render & demo buttons presence
  4. Signup page render & form fields
  5. Failed credential rejection
  6. Successful authentication with seeded demo clinician
  7. Session persistence & clinician profile badge rendering on workstation
  8. 1-Click demo-login API endpoint
  9. New clinician registration workflow
  10. Secure logout & session invalidation
"""

import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from app import app
from auth_db import get_db_connection

def run_tests():
    print("=" * 70)
    print("  MASTHIK ANVESHAN - AUTHENTICATION & ACCESS VERIFICATION")
    print("=" * 70)

    client = app.test_client()
    passed = 0
    total = 0

    def assert_test(name, condition, details=""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f" [PASS] Test {total:02d}: {name}")
        else:
            print(f" [FAIL] Test {total:02d}: {name} - {details}")

    # Test 1: Unauthenticated access to / redirects to /login
    r1 = client.get('/', follow_redirects=False)
    assert_test(
        "Unauthenticated access to '/' redirects to /login",
        r1.status_code == 302 and '/login' in r1.headers.get('Location', ''),
        f"Status: {r1.status_code}, Location: {r1.headers.get('Location')}"
    )

    # Test 2: Unauthenticated access to /pred_page redirects to /login
    r2 = client.get('/pred_page', follow_redirects=False)
    assert_test(
        "Unauthenticated access to '/pred_page' redirects to /login",
        r2.status_code == 302 and '/login' in r2.headers.get('Location', ''),
        f"Status: {r2.status_code}"
    )

    # Test 3: Login page renders with dark glassmorphism and demo access chips
    r3 = client.get('/login')
    html3 = r3.get_data(as_text=True)
    assert_test(
        "Login page renders with 200 OK and demo clinician chips",
        r3.status_code == 200 and 'Clinician Sign In' in html3 and 'Dr. Radhika Muvva, MD' in html3 and 'Instant 1-Click Demo Clinician Access' in html3,
        f"Status: {r3.status_code}"
    )

    # Test 4: Signup page renders with institutional role dropdown
    r4 = client.get('/signup')
    html4 = r4.get_data(as_text=True)
    assert_test(
        "Signup page renders with 200 OK and clinical roles",
        r4.status_code == 200 and 'Clinician Registration' in html4 and 'Neuroradiologist' in html4 and 'regConfirmPassword' in html4,
        f"Status: {r4.status_code}"
    )

    # Test 5: Invalid credentials rejected
    r5 = client.post('/login', data={'email': 'radhika@neuro.ai', 'password': 'wrongpassword'}, follow_redirects=True)
    html5 = r5.get_data(as_text=True)
    assert_test(
        "Invalid password rejected with flash alert",
        'Invalid clinical email or password' in html5,
        "Flash alert not found in response"
    )

    # Test 6: Valid login with demo account
    with client.session_transaction() as sess:
        sess.clear()
    r6 = client.post('/login', data={'email': 'radhika@neuro.ai', 'password': 'password123', 'remember': 'on'}, follow_redirects=False)
    assert_test(
        "Valid login redirects to '/' with 302",
        r6.status_code == 302 and r6.headers.get('Location') in ['/', 'http://localhost/'],
        f"Status: {r6.status_code}, Location: {r6.headers.get('Location')}"
    )

    # Test 7: Authenticated workstation displays clinician profile chip & logout link
    r7 = client.get('/')
    html7 = r7.get_data(as_text=True)
    assert_test(
        "Workstation renders clinician profile chip and logout control",
        r7.status_code == 200 and 'Dr. Radhika Muvva, MD' in html7 and 'Chief Neuroradiologist' in html7 and '/logout' in html7,
        f"Missing clinician badge in HTML"
    )

    # Test 8: 1-Click Demo login endpoint (/api/auth/demo-login)
    r8 = client.post('/api/auth/demo-login', json={'email': 'akshay@masthik.ai'})
    json8 = r8.get_json()
    assert_test(
        "1-Click demo-login API authenticates instantly",
        r8.status_code == 200 and json8.get('status') == 'success' and 'Dr. Akshay Kumar' in json8.get('message', ''),
        f"Response: {json8}"
    )

    # Test 9: Clinician Registration with unique email (clear session first)
    with client.session_transaction() as sess:
        sess.clear()
    test_email = f"tester_{os.getpid()}@neurohospital.org"
    r9 = client.post('/signup', data={
        'name': 'Dr. Marcus Vance, MD',
        'email': test_email,
        'role': 'Neurosurgeon',
        'institution': 'Stanford Neuroscience',
        'password': 'safePassword2026',
        'confirm_password': 'safePassword2026',
        'terms': 'on'
    }, follow_redirects=True)
    html9 = r9.get_data(as_text=True)
    assert_test(
        "Clinician registration creates account and logs in automatically",
        'Dr. Marcus Vance, MD' in html9 and 'Neurosurgeon' in html9,
        "New user profile not rendered in redirected workstation"
    )

    # Test 10: Secure Logout invalidates session
    r10 = client.get('/logout', follow_redirects=True)
    html10 = r10.get_data(as_text=True)
    assert_test(
        "Logout terminates session and redirects to /login",
        'signed out' in html10 and 'Clinician Sign In' in html10,
        "Logout confirmation not found"
    )

    # Test 11: Subsequent access to / is redirected back to /login
    r11 = client.get('/', follow_redirects=False)
    assert_test(
        "Post-logout access to '/' is denied with redirect to /login",
        r11.status_code == 302 and '/login' in r11.headers.get('Location', ''),
        f"Status: {r11.status_code}"
    )

    print("=" * 70)
    print(f"  AUTHENTICATION SUITE RESULTS: {passed}/{total} TESTS PASSED")
    print("=" * 70)

    if passed == total:
        print(" [SUCCESS] All authentication requirements verified and operational.")
        return 0
    else:
        print(f" [FAILURE] {total - passed} tests failed.")
        return 1

if __name__ == '__main__':
    sys.exit(run_tests())
