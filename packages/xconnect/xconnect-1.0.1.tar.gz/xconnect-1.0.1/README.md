# clipSync CLI by XDT Labs

A secure, authenticated, cross-platform clipboard synchronization tool built with Python and Firebase.

## Features
- **Real-time Sync**: Automatically syncs your clipboard across devices.
- **Secure Authentication**: Integrated with Firebase Auth. Collects profile details on first login.
- **SaaS Model**: Includes version control and a remote kill-switch for service management.
- **Cross-Platform**: Works on macOS, Windows, and Linux.

## Installation
```bash
pip install clipsync-xdt
```

## Usage
1. **Login**: Authenticate and set up your profile.
   ```bash
   csync login
   ```
2. **Start Service**: Begin syncing.
   ```bash
   csync serve
   ```
3. **Stop Service**: Stop background sync.
   ```bash
   csync stop
   ```
4. **Logout**:
   ```bash
   csync logout
   ```

## Development
To set up locally:
1. Clone the repository.
2. Install dependencies: `pip install -e .`
3. Deploy Firebase Functions in the `firebase/` directory.

## License
MIT
