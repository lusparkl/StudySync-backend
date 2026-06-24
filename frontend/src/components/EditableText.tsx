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
  }, [value, multiline])

  async function save(rawValue: string) {
    const nextValue = rawValue.trim()
    if (nextValue === value.trim() || disabled) return
    await onSave(nextValue)
  }

  if (multiline) {
    return (
      <div className="editable-wrap">
        <textarea
          key={value}
          ref={textareaRef}
          className={clsx(
            'editable',
            'editable-textarea',
            variant === 'document' && 'editable-document',
          )}
          defaultValue={value}
          placeholder={placeholder}
          disabled={disabled}
          onInput={(event) => resizeTextarea(event.currentTarget)}
          onBlur={(event) => save(event.currentTarget.value)}
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
          title && 'editable-title',
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
