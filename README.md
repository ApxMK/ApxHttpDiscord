# Official documentation for the APX http discord python package.
Please always refer to the "Further development plans" enhancement type issue under github "Issues" section, the "Development schedule" section in the README.md and "Important application notices" section in the README.md to understand the proposed development schedule, the "in progress" development and conditions which may affect the application of the package for your intended use case.

## Development schedule

## Important application notices
Please refer to the discord documentation at: https://discord.com/developers/docs/intro, for more details on the classes.
The documentation in this package aims to be minimal due to the high probability of changing discord documentation on the official site.
However, documentation will be provided to clarify possible instances of misunderstanding when using this package where neccesary.
The msgspec classes in this package are used for the purposes of:
- type validation of JSON data, for example when received from the discord websocket connection or HTTP API endpoints.
- value validation of instantiated msgspec representation classes, conditional on the fields of the classes and
implementing the conditional relations defined in the official documentation for the msgspec classes.
For example,
In the webhook endpoints, the prescence of the files JSON param field indicates that the attachment field should be non-null.
- a serializable interface format for another common data format(e.g msgpack)

### Activity msgspec class
- The Activity msgspec class is excluded from this module, this package intends to model discord HTTP endpoint data structures only and not the gateway websocket structures. 
If you do decide to use the SetActivityArgument class in the RPC discord section, consider writing your own Activity class. 
- Moreover, this package is subject to changes in the foreseeable future, all updates will be viewable from the official github repository.

In the RPC section of this module, the SetActivityArgument class uses the missing Activity msgspec class:
class SetActivityArgument(msgspec.Struct, kw_only=True):
    pid: int  # application's process id
    activity: 'Activity'  # rich presence to assign to the user (limited to Playing, Listening, Watching, or Competing)
