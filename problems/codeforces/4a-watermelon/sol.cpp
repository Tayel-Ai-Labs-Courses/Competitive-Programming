// Codeforces 4A - Watermelon
//
// Split w into two EVEN positive parts. So w must be even, and w must be
// larger than 2 (w = 2 would need 1 + 1, and 1 is odd).
//
// The whole problem is that second condition. Reading "two positive even
// parts" and forgetting that 2 cannot be split is the trap, and the sample
// does not catch it. Read constraints, then read the edge of the range.

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int w;
    cin >> w;
    cout << ((w % 2 == 0 && w > 2) ? "YES" : "NO") << "\n";
    return 0;
}
