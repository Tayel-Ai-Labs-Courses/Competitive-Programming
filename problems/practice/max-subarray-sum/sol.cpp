// Maximum subarray sum - Kadane's algorithm, O(n).
//
// At each index, the best subarray ending here either extends the best
// subarray ending at the previous index, or starts fresh at this element.
// That one sentence is the whole algorithm.
//
//     running = max(running + a[i], a[i])
//
// The bug this file was written with, and that tools/stress.py found on its
// second random test:
//
//     ll best = 0;        // WRONG
//
// Starting `best` at 0 silently claims the empty subarray is allowed. On
// input `1 / -8` it answers 0 where the real answer is -8. The sample tests
// of this kind of problem are almost never all-negative, so this passes the
// samples and fails the judge. Initialise from real data instead.

#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;

    ll best = a[0], running = a[0];
    for (int i = 1; i < n; i++) {
        running = max(running + a[i], a[i]);
        best = max(best, running);
    }
    cout << best << "\n";
    return 0;
}
