# Plugins

sdetkit supports plugin discovery from both entry points and `.sdetkit/plugins.toml`.

```toml
[notify]
my_stdout = "my_pkg.notify:factory"

[ops_tasks]
my_task = "my_pkg.ops:task_factory"
```

Built-in notifier: `sdetkit notify stdout --message "hello"`.
Optional adapters (`telegram`, `whatsapp`) are soft dependencies with friendly configuration errors.
