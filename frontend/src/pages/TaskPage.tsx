import { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react'
import type { FocusEvent, FormEvent, KeyboardEvent, PointerEvent } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  ArrowLeft,
  Bold,
  CheckSquare,
  Code2,
  Eye,
  Heading1,
  List,
  Loader2,
  Pencil,
  Plus,
  Save,
  Trash2,
} from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import clsx from 'clsx'
import remarkGfm from 'remark-gfm'
import { toast } from 'sonner'

import { AppIcon } from '../components/AppIcon'
import { EditableText } from '../components/EditableText'
import { EmptyState } from '../components/EmptyState'
import { ErrorView, LoadingView } from '../components/StatusView'
import { api, apiErrorToMessage, type Note } from '../lib/api'
import { normalizeOptional } from '../lib/format'
import { numberParam } from '../lib/route'

export function TaskPage() {
  const params = useParams()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const workspaceId = numberParam(params.workspaceId)
  const taskId = numberParam(params.taskId)
  const [selectedNoteId, setSelectedNoteId] = useState<number | null>(null)

  const workspaceQuery = useQuery({
    queryKey: ['workspace', workspaceId],
    queryFn: () => api.getWorkspace(workspaceId ?? 0),
    enabled: workspaceId !== null,
  })

  const taskQuery = useQuery({
    queryKey: ['task', taskId],
    queryFn: () => api.getTask(taskId ?? 0),
    enabled: taskId !== null,
  })

  const notesQuery = useQuery({
    queryKey: ['notes', taskId],
    queryFn: () => api.getNotes(taskId ?? 0),
    enabled: taskId !== null,
  })

  const updateTaskMutation = useMutation({
    mutationFn: (payload: { title?: string | null; text?: string | null }) =>
      api.updateTask(taskId ?? 0, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['task', taskId] })
      queryClient.invalidateQueries({ queryKey: ['tasks', workspaceId] })
    },
    onError: (error) => toast.error(apiErrorToMessage(error)),
  })

  const deleteTaskMutation = useMutation({
    mutationFn: () => api.deleteTask(taskId ?? 0),
    onSuccess: () => {
      toast.success('Task deleted')
      queryClient.invalidateQueries({ queryKey: ['tasks', workspaceId] })
      queryClient.invalidateQueries({ queryKey: ['workspace', workspaceId] })
      navigate(`/app/workspaces/${workspaceId}`, { replace: true })
    },
    onError: (error) => toast.error(apiErrorToMessage(error)),
  })

  const updateNoteMutation = useMutation({
    mutationFn: ({
      noteId,
      payload,
    }: {
      noteId: number
      payload: { title?: string | null; text?: string | null }
    }) => api.updateNote(noteId, payload),
    onSuccess: (updatedNote) => {
      queryClient.setQueryData<Note[]>(['notes', taskId], (current) =>
        (current ?? []).map((note) =>
          note.note_id === updatedNote.note_id ? updatedNote : note,
        ),
      )
      queryClient.invalidateQueries({ queryKey: ['notes', taskId] })
    },
    onError: (error) => toast.error(apiErrorToMessage(error)),
  })

  const deleteNoteMutation = useMutation({
    mutationFn: (noteId: number) => api.deleteNote(noteId),
    onSuccess: () => {
      toast.success('Note deleted')
      queryClient.invalidateQueries({ queryKey: ['notes', taskId] })
    },
    onError: (error) => toast.error(apiErrorToMessage(error)),
  })

  const notes = notesQuery.data ?? []
  const selectedNote =
    notes.find((note) => note.note_id === selectedNoteId) ?? notes[0] ?? null
  const activeNoteId = selectedNote?.note_id ?? null

  if (workspaceId === null || taskId === null) {
    return (
      <ErrorView
        title="Task not found"
        message="The workspace or task id in this route is not valid."
      />
    )
  }

  if (taskQuery.isLoading || workspaceQuery.isLoading) {
    return <LoadingView label="Loading task" />
  }

  if (taskQuery.isError || !taskQuery.data) {
    return (
      <ErrorView title="Task not available" message={apiErrorToMessage(taskQuery.error)} />
    )
  }

  const task = taskQuery.data

  async function saveTaskTitle(nextTitle: string) {
    if (!nextTitle) {
      toast.error('Task title cannot be empty')
      return
    }

    await updateTaskMutation.mutateAsync({ title: nextTitle })
  }

  function deleteTask() {
    const confirmed = window.confirm(`Delete "${task.title}" and its notes?`)
    if (!confirmed) return
    deleteTaskMutation.mutate()
  }

  return (
    <article className="page task-page">
      <header className="task-header">
        <Link className="breadcrumb-link" to={`/app/workspaces/${workspaceId}`}>
          <ArrowLeft size={16} />
          {workspaceQuery.data?.title ?? 'Workspace'}
        </Link>
        <button
          type="button"
          className="button button-danger"
          onClick={deleteTask}
          disabled={deleteTaskMutation.isPending}
        >
          <Trash2 size={16} />
          Delete task
        </button>
      </header>

      <section className="task-document">
        <div className="page-kicker">
          <AppIcon name="task" size={22} />
          Task
        </div>
        <EditableText
          value={task.title}
          placeholder="Untitled task"
          title
          saving={updateTaskMutation.isPending}
          onSave={saveTaskTitle}
        />
        <EditableText
          value={task.text ?? ''}
          placeholder="Add study instructions, acceptance criteria, or links..."
          multiline
          saving={updateTaskMutation.isPending}
          onSave={(value) =>
            updateTaskMutation.mutateAsync({ text: normalizeOptional(value) })
          }
        />
      </section>

      <section className="notes-layout">
        <aside className="notes-sidebar">
          <div className="section-heading compact">
            <div>
              <p className="eyebrow">Docs</p>
              <h2>Notes</h2>
            </div>
            <span>{notes.length}</span>
          </div>

          <NewNoteComposer taskId={task.task_id} onCreated={setSelectedNoteId} />

          {notesQuery.isLoading ? <LoadingView label="Loading notes" /> : null}

          {!notesQuery.isLoading && notes.length === 0 ? (
            <EmptyState
              icon={<AppIcon name="note" size={34} />}
              title="No notes"
              description="Add a lightweight doc for formulas, resources, or explanations."
            />
          ) : null}

          <div className="note-list">
            {notes.map((note) => (
              <button
                key={note.note_id}
                type="button"
                className={clsx(
                  'note-list-item',
                  note.note_id === activeNoteId && 'active',
                )}
                onClick={() => setSelectedNoteId(note.note_id)}
              >
                <AppIcon name="note" size={22} />
                <span>
                  <strong>{note.title}</strong>
                  <small>{note.text || 'Empty note'}</small>
                </span>
              </button>
            ))}
          </div>
        </aside>

        <NoteEditor
          key={selectedNote?.note_id ?? 'empty'}
          note={selectedNote}
          deleting={deleteNoteMutation.isPending}
          onSave={(note, payload) =>
            updateNoteMutation.mutateAsync({
              noteId: note.note_id,
              payload,
            })
          }
          onDelete={(note) => {
            const confirmed = window.confirm(`Delete "${note.title}"?`)
            if (!confirmed) return
            deleteNoteMutation.mutate(note.note_id)
          }}
        />
      </section>
    </article>
  )
}

function NewNoteComposer({
  taskId,
  onCreated,
}: {
  taskId: number
  onCreated: (noteId: number) => void
}) {
  const queryClient = useQueryClient()
  const [title, setTitle] = useState('')

  const createNoteMutation = useMutation({
    mutationFn: () =>
      api.createNote(taskId, {
        title: title.trim() || 'Untitled note',
        text: null,
      }),
    onSuccess: (note) => {
      toast.success('Note created')
      queryClient.setQueryData<Note[]>(['notes', taskId], (current) => [
        ...(current ?? []),
        note,
      ])
      queryClient.invalidateQueries({ queryKey: ['notes', taskId] })
      setTitle('')
      onCreated(note.note_id)
    },
    onError: (error) => toast.error(apiErrorToMessage(error)),
  })

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    createNoteMutation.mutate()
  }

  return (
    <form className="note-composer" onSubmit={submit}>
      <input
        value={title}
        onChange={(event) => setTitle(event.target.value)}
        placeholder="New note"
        aria-label="New note title"
      />
      <button
        type="submit"
        className="icon-button"
        aria-label="Add note"
        title="Add note"
        disabled={createNoteMutation.isPending}
      >
        <Plus size={16} />
      </button>
    </form>
  )
}

function NoteEditor({
  note,
  deleting,
  onSave,
  onDelete,
}: {
  note: Note | null
  deleting: boolean
  onSave: (
    note: Note,
    payload: { title?: string | null; text?: string | null },
  ) => Promise<unknown>
  onDelete: (note: Note) => void
}) {
  if (!note) {
    return (
      <section className="note-editor empty-note-editor">
        <EmptyState
          icon={<AppIcon name="note" size={34} />}
          title="Select a note"
          description="Notes you create for this task will open here."
        />
      </section>
    )
  }

  return (
    <section className="note-editor" aria-label="Note editor">
      <NoteDocumentEditor note={note} deleting={deleting} onSave={onSave} onDelete={onDelete} />
    </section>
  )
}

type SaveStatus = 'saved' | 'saving' | 'unsaved' | 'error'
type NoteMode = 'write' | 'preview'

function NoteDocumentEditor({
  note,
  deleting,
  onSave,
  onDelete,
}: {
  note: Note
  deleting: boolean
  onSave: (
    note: Note,
    payload: { title?: string | null; text?: string | null },
  ) => Promise<unknown>
  onDelete: (note: Note) => void
}) {
  const [title, setTitle] = useState(note.title)
  const [text, setText] = useState(note.text ?? '')
  const [savedTitle, setSavedTitle] = useState(note.title)
  const [savedText, setSavedText] = useState(note.text ?? '')
  const [status, setStatus] = useState<SaveStatus>('saved')
  const [mode, setMode] = useState<NoteMode>((note.text ?? '').trim() ? 'preview' : 'write')
  const documentRef = useRef<HTMLDivElement | null>(null)
  const textareaRef = useRef<HTMLTextAreaElement | null>(null)
  const focusTextareaRef = useRef(false)
  const skipPreviewOnBlurRef = useRef(false)

  const normalizedTitle = title.trim() || 'Untitled note'
  const hasChanges = normalizedTitle !== savedTitle.trim() || text !== savedText

  useLayoutEffect(() => {
    const textarea = textareaRef.current
    if (!textarea) return

    textarea.style.height = 'auto'
    textarea.style.height = `${textarea.scrollHeight}px`

    if (mode === 'write' && focusTextareaRef.current) {
      focusTextareaRef.current = false
      textarea.focus()
      textarea.setSelectionRange(text.length, text.length)
    }
  }, [mode, text])

  const saveNow = useCallback(async () => {
    const nextTitle = normalizedTitle
    const nextText = text.trim().length > 0 ? text : null
    const titleChanged = nextTitle !== savedTitle.trim()
    const textChanged = text !== savedText

    if (!titleChanged && !textChanged) {
      setStatus('saved')
      return
    }

    setStatus('saving')

    try {
      await onSave(note, {
        ...(titleChanged ? { title: nextTitle } : {}),
        ...(textChanged ? { text: nextText } : {}),
      })
      setSavedTitle(nextTitle)
      setSavedText(text)
      setStatus('saved')
    } catch (error) {
      setStatus('error')
      toast.error(apiErrorToMessage(error))
    }
  }, [normalizedTitle, note, onSave, savedText, savedTitle, text])

  useEffect(() => {
    if (!hasChanges) return undefined

    const timeoutId = window.setTimeout(() => {
      void saveNow()
    }, 900)

    return () => window.clearTimeout(timeoutId)
  }, [hasChanges, saveNow])

  function updateTitle(nextTitle: string) {
    setTitle(nextTitle)
    setStatus('unsaved')
  }

  function updateText(nextText: string) {
    setText(nextText)
    setStatus('unsaved')
  }

  function handleShortcut(event: KeyboardEvent<HTMLInputElement | HTMLTextAreaElement>) {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 's') {
      event.preventDefault()
      void saveNow()
    }
  }

  function switchMode(nextMode: NoteMode, options?: { focusBody?: boolean }) {
    if (nextMode === 'write' && options?.focusBody) {
      focusTextareaRef.current = true
    }

    setMode(nextMode)
    if (nextMode === 'preview') {
      void saveNow()
    }
  }

  function handleDocumentBlur(event: FocusEvent<HTMLDivElement>) {
    const nextTarget = event.relatedTarget

    if (nextTarget instanceof Node && event.currentTarget.contains(nextTarget)) {
      return
    }

    if (skipPreviewOnBlurRef.current) {
      return
    }

    void saveNow()
    setMode('preview')
  }

  function handlePreviewPointerDown(event: PointerEvent<HTMLDivElement>) {
    if (event.target instanceof Element && event.target.closest('a')) {
      return
    }

    event.preventDefault()
    skipPreviewOnBlurRef.current = true
    switchMode('write', { focusBody: true })
    window.requestAnimationFrame(() => {
      skipPreviewOnBlurRef.current = false
    })
  }

  function insertSnippet(kind: 'bold' | 'heading' | 'list' | 'todo' | 'code') {
    const textarea = textareaRef.current
    if (!textarea) return

    const start = textarea.selectionStart
    const end = textarea.selectionEnd
    const selectedText = text.slice(start, end)
    let nextText = text
    let nextSelectionStart = start
    let nextSelectionEnd = end

    if (kind === 'bold') {
      const fallback = selectedText || 'bold text'
      nextText = `${text.slice(0, start)}**${fallback}**${text.slice(end)}`
      nextSelectionStart = start + 2
      nextSelectionEnd = nextSelectionStart + fallback.length
    }

    if (kind === 'heading') {
      const lineStart = text.lastIndexOf('\n', start - 1) + 1
      nextText = `${text.slice(0, lineStart)}# ${text.slice(lineStart)}`
      nextSelectionStart = start + 2
      nextSelectionEnd = end + 2
    }

    if (kind === 'list' || kind === 'todo') {
      const marker = kind === 'todo' ? '- [ ] ' : '- '
      const lineStart = text.lastIndexOf('\n', start - 1) + 1
      nextText = `${text.slice(0, lineStart)}${marker}${text.slice(lineStart)}`
      nextSelectionStart = start + marker.length
      nextSelectionEnd = end + marker.length
    }

    if (kind === 'code') {
      const fallback = selectedText || 'code'
      const block = `\`\`\`\n${fallback}\n\`\`\``
      nextText = `${text.slice(0, start)}${block}${text.slice(end)}`
      nextSelectionStart = start + 4
      nextSelectionEnd = nextSelectionStart + fallback.length
    }

    updateText(nextText)
    window.requestAnimationFrame(() => {
      textarea.focus()
      textarea.setSelectionRange(nextSelectionStart, nextSelectionEnd)
    })
  }

  function handleTextKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    handleShortcut(event)

    if (event.key === 'Tab') {
      event.preventDefault()
      const textarea = event.currentTarget
      const start = textarea.selectionStart
      const end = textarea.selectionEnd
      const nextText = `${text.slice(0, start)}  ${text.slice(end)}`
      updateText(nextText)
      window.requestAnimationFrame(() => {
        textarea.setSelectionRange(start + 2, start + 2)
      })
    }
  }

  return (
    <div ref={documentRef} className="note-document" onBlur={handleDocumentBlur}>
      <div className="note-editor-actions">
        <div className="note-status" data-status={status}>
          {status === 'saving' ? <Loader2 className="spin" size={14} /> : <Save size={14} />}
          <span>
            {status === 'saving'
              ? 'Saving'
              : status === 'unsaved'
                ? 'Unsaved'
                : status === 'error'
                  ? 'Could not save'
                  : 'Saved'}
          </span>
        </div>
        <div className="note-action-cluster">
          {mode === 'write' ? (
            <div className="markdown-toolbar" aria-label="Markdown tools">
              <button
                type="button"
                className="icon-button"
                title="Heading"
                onClick={() => insertSnippet('heading')}
              >
                <Heading1 size={16} />
              </button>
              <button
                type="button"
                className="icon-button"
                title="Bold"
                onClick={() => insertSnippet('bold')}
              >
                <Bold size={16} />
              </button>
              <button
                type="button"
                className="icon-button"
                title="List"
                onClick={() => insertSnippet('list')}
              >
                <List size={16} />
              </button>
              <button
                type="button"
                className="icon-button"
                title="Checklist"
                onClick={() => insertSnippet('todo')}
              >
                <CheckSquare size={16} />
              </button>
              <button
                type="button"
                className="icon-button"
                title="Code block"
                onClick={() => insertSnippet('code')}
              >
                <Code2 size={16} />
              </button>
            </div>
          ) : null}
          <div className="note-mode-toggle" aria-label="Note mode">
            <button
              type="button"
              className={clsx(mode === 'write' && 'active')}
              onClick={() => switchMode('write', { focusBody: true })}
            >
              <Pencil size={14} />
              Write
            </button>
            <button
              type="button"
              className={clsx(mode === 'preview' && 'active')}
              onClick={() => switchMode('preview')}
            >
              <Eye size={14} />
              Preview
            </button>
          </div>
          <button
            type="button"
            className="icon-button danger-icon"
            onClick={() => onDelete(note)}
            disabled={deleting}
            aria-label="Delete note"
            title="Delete note"
          >
            <Trash2 size={16} />
          </button>
        </div>
      </div>

      <input
        className="note-title-input"
        value={title}
        placeholder="Untitled note"
        aria-label="Note title"
        onFocus={() => switchMode('write')}
        onChange={(event) => updateTitle(event.target.value)}
        onKeyDown={handleShortcut}
      />

      {mode === 'write' ? (
        <textarea
          ref={textareaRef}
          className="note-body-input"
          value={text}
          placeholder="Write notes, links, formulas, and reminders..."
          aria-label="Note text"
          spellCheck
          onFocus={() => switchMode('write')}
          onChange={(event) => updateText(event.target.value)}
          onKeyDown={handleTextKeyDown}
        />
      ) : (
        <div className="markdown-preview" onPointerDown={handlePreviewPointerDown}>
          {text.trim() ? (
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{text}</ReactMarkdown>
          ) : (
            <p className="markdown-empty">Empty note</p>
          )}
        </div>
      )}
    </div>
  )
}
