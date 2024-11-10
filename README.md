# touchy
`touch` utility but with file templates.

## Config file format
`~.touchy`
```yaml
verbose: true
paths: 
  default:
    - filename: README.md
      content: |
        # {{dirname}}
    - filename: .gitignore
      content: |
        build/**
        {{dirname}}.egg-info/**
  /home/tsp/website:
    - filename: "*.md"
      content: |
        ---
        title: "{{filename}}"
        date: {{isotimestamp}}
        draft: true
        ---
    - filename: "*.txt"
      content: |
        test txt file
```

* `{{isotimestamp}}` - Replaces with current time in `%Y-%m-%dT%H:%M:%SZ` format
* `{{filename}}` - Filename without extension 
* `{{dirname}}` - Folder the file is being created in
