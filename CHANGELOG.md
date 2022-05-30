# CHANGELOG

## [Unreleased]

### Changes

- Added ability to update the actual device name via SimpleMDM (#24, #38) ([@bryanheinz](https://github.com/bryanheinz))
- Replaced get_logs() `id_override` input parameter with `starting_after` and `limit` (#25) ([@bryanheinz](https://github.com/bryanheinz))
- Fixes calls that return a single item (#26) ([@MagerValp](https://github.com/MagerValp))
- Add method to download profiles (#40) ([@joncrain](https://github.com/joncrain))
- Adds option for get_devices to include_awaiting_enrollment (#43) ([@joncrain](https://github.com/joncrain))
- Fixes `Devices.delete_device()` ([@MagerValp](https://github.com/MagerValp))
- Add Devices methods for enabling/disabling remote desktop, and profile and user listing ([@MagerValp](https://github.com/MagerValp))
- Add /devices request rate limiting to `_get_data` ([@MagerValp](https://github.com/MagerValp))
- Add retry on 5xx errors to GET requests to `_get_data` ([@MagerValp](https://github.com/MagerValp))

### Issues

- Closes issue #24
- Closes issue #38
- Closes issue #25
- Closes issue #26
- Closes issue #40
- Closes issue #43

## [v3.0.6]

### PRs Included

- [#35](https://github.com/macadmins/simpleMDMpy/pull/25)
- [#34](https://github.com/macadmins/simpleMDMpy/pull/34)
- [#27](https://github.com/macadmins/simpleMDMpy/pull/27)

### Changes

- Add method to get all custom attributes for a device

## [v3.0.5]

### Issues

- Closes #21

### Added 

- CODEOWNERS

## [v3.0.4]

### Issues

- Closes #19
- Closes #18

### Added

- LICENSE
- `Contributing.md`

### Changed

- Merged with @MagerValp / simpleMDMpy @ [508540928](https://github.com/MagerValp/simpleMDMpy/commit/50854094bee2ac5306eded7c5614d76f3eab4c25)
- minor tweaks on the readme

## [v3.0.3]

### Issues

- Closes #15
- Closed #16
- Closed #14

### Added

- support for setting custom attr on initial creation
- support for updating a custom attribute

### Changed

- default branch is now `main`
- remove `data` payload from Devices.delete_device

## [v3.0.2]

### Issues

- Closes #11
- Closes #12

### Added

- _get_data now has `id_override=None` so you can override `&starting_after=` as you wish
- `id_override=0` implemented in Logs get_logs()

### Changed

- Changed paginaition to work without compounding to a `414`

## [v3.0.1]

### Issues

- Closes #9

## Changed

- Changed paginaition to work, now returns obj not response
- good catch @bryanheinz

## [v3.0.0]

- Closes #3

## Changed

- removed forced encoding for `GET` responses
- added some pylint comments

## [v2.1.0]

### Issues

- Closes #5

### Changed

- fixed module names

## [v2.0.0]

### Issues

- Closes #1

### Added

- Partial/Full Support for:
  - Assignment Groups
  - Custom Attributes
  - Custom Configuration
  - DEP Servers
  - Enrollments
  - Logs
  - Lost Mode
  - Webhooks
- (Somewhat) Help(ful) Strings

### Changed

- removed PIP items for now

### Base

- forked from [SteveKueng/simple_mdm_py](https://github.com/SteveKueng/simple_mdm_py/blob/master/setup.py) at [cf6650f](https://github.com/SteveKueng/simpleMDMpy/commit/cf6650fe72220577abd5c654d03476c88b81bcb0)
