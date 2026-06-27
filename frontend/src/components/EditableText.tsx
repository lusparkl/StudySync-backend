import { useLayoutEffect, useRef } from 'react'
import { Loader2 } from 'lucide-react'
import clsx from 'clsx'

type EditableTextProps = {
  value: string
  placeholder: string
  multiline?: boolean
  title?: boolean
  disabled?: boolean
  saving?: boolean
  variant?: 'field' | 'document'
  onSave: (value: string) => Promise<unknown> | unknown
}

export function EditableText({
  value,
  placeholder,
  multiline = false,
  title = false,
  disabled = false,
  saving = false,
  variant = 'field',
  onSave,
}: EditableTextProps) {
  const textareaRef = useRef<HTMLTextAreaElement | null>(null)

  function resizeTextarea(textarea: HTMLTextAreaElement) {
    textarea.style.height = 'auto'
    textarea.style.height = `${textarea.scrollHeight}px`
  }

  useLayoutEffect(() => {
    if (!textareaRef.current) return
    resizeTextarea(textareaRef.current)
  }, [value, multiline, title])

  async function save(rawValue: string) {
    const nextValue = title
      ? rawValue.replace(/\s+/g, ' ').trim()
      : rawValue.trim()
    if (nextValue === value.trim() || disabled) return
    await onSave(nextValue)
  }

  if (multiline || title) {
    return (
      <div className="editable-wrap">
        <textarea
          key={value}
          ref={textareaRef}
          className={clsx(
            'editable',
            multiline && 'editable-textarea',
            title && 'editable-title',
            variant === 'document' && 'editable-document',
          )}
          defaultValue={value}
          placeholder={placeholder}
          disabled={disabled}
          rows={1}
          onInput={(event) => resizeTextarea(event.currentTarget)}
          onBlur={(event) => save(event.currentTarget.value)}
          onKeyDown={(event) => {
            if (title && event.key === 'Enter') {
              event.preventDefault()
              event.currentTarget.blur()
            }
          }}
        />
        {saving ? <Loader2 className="inline-spinner spin" size={16} /> : null}
      </div>
    )
  }

  return (
    <div className="editable-wrap">
      <input
        key={value}
        className={clsx(
          'editable',
          variant === 'document' && 'editable-document',
        )}
        defaultValue={value}
        placeholder={placeholder}
        disabled={disabled}
        onBlur={(event) => save(event.currentTarget.value)}
        onKeyDown={(event) => {
          if (event.key === 'Enter') {
            event.currentTarget.blur()
          }
        }}
      />
      {saving ? <Loader2 className="inline-spinner spin" size={16} /> : null}
    </div>
  )
}
