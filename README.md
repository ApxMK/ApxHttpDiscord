# Official documentation for the APX http discord python package.
- Please refer to the "Further development plans" enhancement type issue under github "Issues" section for further understanding of the proposed future feature development plans.
- [Development schedule](#development-schedule) section in the README.md for the "in progress" feature development.
- [Important application notices](#important-application-notices) section in the README.md for the non-exhaustive list of conditions which may affect the application of the package for your intended use case.
- This package is subject to changes in the foreseeable future, all updates will be viewable from the official github repository.
- Join the official discord to receive notifications on updates to the package:
https://discord.gg/Z63gxmFx
- If you're interested in becoming a contributor, please do so by applying in the official discord for this package; a registeration process will be explained thereafter. All donations and sponsorship funds will be shared amongst contributors proportional to the amount of work contributed. Lastly, details of the procedure for creating new github issues(e.g structure) will be outlined in the discord.
- Please consider that this package is public, maintained free of charge by our contributors who work hard to keep the package functional. The upmost gratitude is given to those who sponsor and donate funds to keep the project ongoing. A memorial section will be viewable in the discord to honor our supporters.

# Table of Contents
- [Design decisions](#design-decisions)
- [Development schedule](#development-schedule)
- [Important application notices](#important-application-notices)
  - [Discord Activity class](#discord-activity-class)
  - [Snowflake fields](#snowflake-fields)

## Design decisions

## Development schedule

## Important application notices
- Please refer to the discord documentation at: https://discord.com/developers/docs/intro, for more details on the msgspec classes.
- The documentation in this package aims to be minimal due to the high probability of changing discord documentation on the official site.
- However, documentation will be provided to clarify possible instances of misunderstanding when using this package where neccesary.
- The msgspec classes in this package are used for the purposes of:
    - type validation of JSON data, for example when received from the discord websocket connection or HTTP API endpoints.
    - value validation of instantiated msgspec representation classes, conditional on the fields of the classes and
    implementing the conditional relations defined in the official documentation for the msgspec classes.
    For example,
    In the webhook endpoints, the prescence of the files JSON param field indicates that the attachment field should be non-null.
    - a serializable interface format for another common data format(e.g msgpack)

###### Discord Activity class
- The package directly avoids modelling discord gateway websocket structures. 
- As a result, the Activity msgspec class implementation of the Discord Activity class is excluded from this package.
- If you should decide to use the discord Activity class(e.g in SetActivityArgument class of the RPC discord section), consider writing your own Activity msgspec class. 
- In the RPC section of this module, the SetActivityArgument class uses the missing Activity msgspec class:
  class SetActivityArgument(msgspec.Struct, kw_only=True):
      pid: int  # application's process id
        activity: 'Activity'  # rich presence to assign to the user (limited to Playing, Listening, Watching, or Competing)

###### Generic classes
- Generic classes are classes which are suitable for both serilization into JSON for sending to discord or deserialization from JSON to the generic msgspec class itself.
- As a result, reducing the creation of multiple classes which have the same fields but differing by the abscence of some fields.
- However, producing a problem of undetectable field optionality changes during discord server updates.
e.g If a generic class satisfies class A and class B, whereby the generic class can be instantiated to an instance of class A or class B. If such an update occurs by discord to the optionality property of datatable fields, then ApxHttpDiscord cannot determine a discrepancy during type validation of the generic msgspec class.
- It therefore becomes important to employ "dynamic value error detection" for attribute accesses on instances of the generic msgspec class.

###### Snowflake fields
- Snowflake fields in the discord data tables are implemented in msgspec classes as 'str' rather than 'int'. Remember to convert snowflake field values from 'str' to 'int' before using them in your application.
  
