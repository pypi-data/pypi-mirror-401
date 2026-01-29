/**
 * DocumentModal - Full-screen modal for viewing complete document content
 *
 * Features:
 * - Full metadata display (file type, size, dates, collections, custom metadata)
 * - Beautiful markdown rendering with theme colors
 * - Fully scrollable content
 * - Human review toggle to mark documents as reviewed
 * - Consistent styling across all document views
 */

import { useState, useEffect } from 'react';
import { Modal, ScrollArea, Text, Badge, Group, Box, Divider, Paper, Stack, Switch, Loader, Button } from '@mantine/core';
import { IconFile, IconUserCheck, IconPlus, IconX } from '@tabler/icons-react';
import ReactMarkdown from 'react-markdown';
import type { Document, Collection } from '../types';
import { updateDocumentReview, listCollections, getDocument, manageCollectionLink } from '../ragApi';
import { LinkToCollectionModal } from './modals/LinkToCollectionModal';

interface DocumentModalProps {
  document: Document | null;
  opened: boolean;
  onClose: () => void;
  onDocumentUpdate?: (updatedDocument: Document) => void;
}

export default function DocumentModal({ document, opened, onClose, onDocumentUpdate }: DocumentModalProps) {
  // Local state for reviewed_by_human toggle
  const [isReviewed, setIsReviewed] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);
  const [updateError, setUpdateError] = useState<string | null>(null);

  // Link to collection modal state
  const [isLinkModalOpen, setIsLinkModalOpen] = useState(false);
  const [availableCollections, setAvailableCollections] = useState<Collection[]>([]);
  const [unlinkingCollection, setUnlinkingCollection] = useState<string | null>(null);
  const [unlinkError, setUnlinkError] = useState<string | null>(null);

  // Sync local state with document prop
  useEffect(() => {
    if (document) {
      setIsReviewed(document.reviewed_by_human ?? false);
      setUpdateError(null);
      setUnlinkError(null);
      setUnlinkingCollection(null);
    }
  }, [document]);

  // Load collections when modal opens
  useEffect(() => {
    if (opened) {
      listCollections().then(setAvailableCollections).catch(console.error);
    }
  }, [opened]);

  // Handle successful link - refresh document to show updated collections
  const handleLinkSuccess = async () => {
    if (!document) return;
    try {
      const updated = await getDocument(document.id);
      onDocumentUpdate?.(updated);
    } catch (err) {
      console.error('Failed to refresh document:', err);
    }
    setIsLinkModalOpen(false);
  };

  if (!document) return null;

  // Detect if content is markdown based on file type or content patterns
  const isMarkdown = document.file_type === 'md' ||
                     document.filename.endsWith('.md') ||
                     document.content.includes('# ') ||
                     document.content.includes('## ');

  // Handle review toggle
  const handleReviewToggle = async (checked: boolean) => {
    setIsUpdating(true);
    setUpdateError(null);
    try {
      await updateDocumentReview(document.id, checked);
      setIsReviewed(checked);
      // Notify parent of update if callback provided
      if (onDocumentUpdate) {
        onDocumentUpdate({ ...document, reviewed_by_human: checked });
      }
    } catch (error) {
      setUpdateError(error instanceof Error ? error.message : 'Failed to update review status');
      // Revert the toggle on error
      setIsReviewed(!checked);
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <>
    <Modal
      opened={opened}
      onClose={onClose}
      title={
        <Group gap="xs">
          <IconFile size={20} color="var(--amber)" />
          <Text fw={500} style={{ color: 'var(--amber)' }}>{document.filename}</Text>
          <Badge
            variant="light"
            color="orange"
            size="sm"
          >
            {document.file_type.toUpperCase()}
          </Badge>
        </Group>
      }
      size="xl"
      fullScreen
      styles={{
        content: {
          background: 'var(--charcoal)',
        },
        header: {
          background: 'var(--charcoal-light)',
          borderBottom: '2px solid var(--amber-dark)',
        },
        title: {
          width: '100%',
        },
      }}
    >
      <ScrollArea style={{ height: 'calc(100vh - 80px)' }} offsetScrollbars>
        <Box p="lg">
          {/* Metadata Section */}
          <Paper
            p="md"
            mb="lg"
            style={{
              background: 'var(--charcoal-light)',
              border: '1px solid var(--warm-gray)',
            }}
          >
            <Stack gap="md">
              {/* File Info Row */}
              <Group gap="xl">
                <Box>
                  <Text size="xs" c="dimmed" fw={600} mb={4}>
                    File Type
                  </Text>
                  <Badge
                    variant="light"
                    size="sm"
                    style={{
                      background: 'rgba(245, 158, 11, 0.12)',
                      color: 'var(--amber)',
                    }}
                  >
                    {document.file_type}
                  </Badge>
                </Box>
                <Box>
                  <Text size="xs" c="dimmed" fw={600} mb={4}>
                    File Size
                  </Text>
                  <Text size="sm" c="var(--cream)">
                    {(document.file_size / 1024).toFixed(2)} KB
                  </Text>
                </Box>
                <Box>
                  <Text size="xs" c="dimmed" fw={600} mb={4}>
                    Created
                  </Text>
                  <Text size="sm" c="var(--cream)">
                    {new Date(document.created_at).toLocaleDateString()}
                  </Text>
                </Box>
                {document.updated_at && document.updated_at !== document.created_at && (
                  <Box>
                    <Text size="xs" c="dimmed" fw={600} mb={4}>
                      Updated
                    </Text>
                    <Text size="sm" c="var(--cream)">
                      {new Date(document.updated_at).toLocaleDateString()}
                    </Text>
                  </Box>
                )}
              </Group>

              {/* Collections */}
              <Box>
                <Text size="xs" c="dimmed" fw={600} mb={4}>
                  Collections
                </Text>
                <Group gap="xs">
                  {document.collections?.map((collection) => {
                    const isUnlinking = unlinkingCollection === collection;
                    const canUnlink = document.collections && document.collections.length > 1 && !isUnlinking;

                    return (
                      <Badge
                        key={collection}
                        variant="light"
                        size="sm"
                        style={{
                          background: 'rgba(20, 184, 166, 0.12)',
                          color: 'var(--teal-light)',
                          cursor: canUnlink ? 'pointer' : 'not-allowed',
                          paddingRight: canUnlink ? '4px' : undefined,
                          opacity: isUnlinking ? 0.5 : 1,
                        }}
                        rightSection={
                          canUnlink ? (
                            <IconX
                              size={12}
                              style={{ cursor: 'pointer' }}
                              onClick={async (e) => {
                                e.stopPropagation();
                                setUnlinkingCollection(collection);
                                setUnlinkError(null);
                                try {
                                  await manageCollectionLink(document.id, collection, true);
                                  // Refresh document to get updated collections list
                                  const updated = await getDocument(document.id);
                                  onDocumentUpdate?.(updated);
                                } catch (err) {
                                  const errorMsg = err instanceof Error ? err.message : 'Failed to unlink';
                                  setUnlinkError(errorMsg);
                                  console.error('Unlink failed:', err);
                                } finally {
                                  setUnlinkingCollection(null);
                                }
                              }}
                            />
                          ) : isUnlinking ? (
                            <Loader size={10} color="teal" />
                          ) : undefined
                        }
                      >
                        {collection}
                      </Badge>
                    );
                  })}
                  <Button
                    variant="light"
                    size="xs"
                    color="teal"
                    leftSection={<IconPlus size={14} />}
                    onClick={() => setIsLinkModalOpen(true)}
                  >
                    Add to Collection
                  </Button>
                </Group>
                {document.collections?.length === 1 && (
                  <Text size="xs" c="dimmed" mt={4}>
                    Cannot remove last collection (orphan protection)
                  </Text>
                )}
                {unlinkError && (
                  <Text size="xs" c="red" mt={4}>{unlinkError}</Text>
                )}
              </Box>

              {/* Human Review Status */}
              <Box>
                <Text size="xs" c="dimmed" fw={600} mb={4}>
                  Human Review
                </Text>
                <Group gap="sm" align="center">
                  <Switch
                    checked={isReviewed}
                    onChange={(event) => handleReviewToggle(event.currentTarget.checked)}
                    disabled={isUpdating}
                    color="teal"
                    size="sm"
                    thumbIcon={isUpdating ? <Loader size={10} color="gray" /> : undefined}
                    label={
                      <Group gap={4}>
                        <IconUserCheck size={14} style={{ color: isReviewed ? 'var(--teal-light)' : 'var(--warm-gray)' }} />
                        <Text size="xs" c={isReviewed ? 'var(--teal-light)' : 'var(--warm-gray)'}>
                          {isReviewed ? 'Reviewed' : 'Not reviewed'}
                        </Text>
                      </Group>
                    }
                  />
                  {updateError && (
                    <Text size="xs" c="red">{updateError}</Text>
                  )}
                </Group>
              </Box>

              {/* Evaluation */}
              {document.quality_score !== undefined && (
                <Box>
                  <Text size="xs" c="dimmed" fw={600} mb={4}>
                    Evaluation
                  </Text>
                  <Group gap="xl">
                    <Box>
                      <Text size="xs" c="dimmed" mb={2}>Quality</Text>
                      <Badge
                        variant="light"
                        size="sm"
                        style={{
                          background: document.quality_score >= 0.7
                            ? 'rgba(34, 197, 94, 0.15)'
                            : document.quality_score >= 0.4
                            ? 'rgba(245, 158, 11, 0.15)'
                            : 'rgba(239, 68, 68, 0.15)',
                          color: document.quality_score >= 0.7
                            ? '#22c55e'
                            : document.quality_score >= 0.4
                            ? 'var(--amber)'
                            : '#ef4444',
                        }}
                      >
                        {Math.round(document.quality_score * 100)}%
                      </Badge>
                    </Box>
                    {/* Topic Provided - show the topic string if available */}
                    <Box>
                      <Text size="xs" c="dimmed" mb={2}>Topic Provided</Text>
                      {document.topic_provided ? (
                        <Text size="xs" c="var(--cream)">{document.topic_provided}</Text>
                      ) : (
                        <Badge
                          variant="light"
                          size="sm"
                          style={{
                            background: 'rgba(128, 128, 128, 0.15)',
                            color: 'var(--warm-gray)',
                          }}
                        >
                          None
                        </Badge>
                      )}
                    </Box>
                    {/* Topic Relevance Score - show percentage if evaluated, "Not evaluated" if null */}
                    <Box>
                      <Text size="xs" c="dimmed" mb={2}>Topic Relevance</Text>
                      {document.topic_relevance_score !== null && document.topic_relevance_score !== undefined ? (
                        <Badge
                          variant="light"
                          size="sm"
                          style={{
                            background: document.topic_relevance_score >= 0.7
                              ? 'rgba(34, 197, 94, 0.15)'
                              : document.topic_relevance_score >= 0.4
                              ? 'rgba(245, 158, 11, 0.15)'
                              : 'rgba(239, 68, 68, 0.15)',
                            color: document.topic_relevance_score >= 0.7
                              ? '#22c55e'
                              : document.topic_relevance_score >= 0.4
                              ? 'var(--amber)'
                              : '#ef4444',
                          }}
                        >
                          {Math.round(document.topic_relevance_score * 100)}%
                        </Badge>
                      ) : (
                        <Badge
                          variant="light"
                          size="sm"
                          style={{
                            background: 'rgba(128, 128, 128, 0.15)',
                            color: 'var(--warm-gray)',
                          }}
                        >
                          Not evaluated
                        </Badge>
                      )}
                    </Box>
                    {document.eval_model && (
                      <Box>
                        <Text size="xs" c="dimmed" mb={2}>Model</Text>
                        <Text size="xs" c="var(--cream-dim)">{document.eval_model}</Text>
                      </Box>
                    )}
                  </Group>
                  {document.quality_summary && (
                    <Text size="xs" c="var(--cream-dim)" mt="xs" style={{ fontStyle: 'italic' }}>
                      {document.quality_summary}
                    </Text>
                  )}
                </Box>
              )}

              {/* Custom Metadata */}
              {document.metadata && Object.keys(document.metadata).length > 0 && (
                <Box>
                  <Text size="xs" c="dimmed" fw={600} mb={4}>
                    Custom Metadata
                  </Text>
                  <Paper
                    p="xs"
                    style={{
                      background: 'var(--charcoal)',
                      border: '1px solid var(--charcoal-lighter)',
                      maxHeight: '150px',
                      overflowY: 'auto',
                    }}
                  >
                    <pre
                      style={{
                        margin: 0,
                        fontSize: '11px',
                        fontFamily: 'Fira Code, monospace',
                        color: 'var(--cream-dim)',
                      }}
                    >
                      {JSON.stringify(document.metadata, null, 2)}
                    </pre>
                  </Paper>
                </Box>
              )}
            </Stack>
          </Paper>

          <Divider
            mb="lg"
            label={
              <Text size="xs" fw={600} c="dimmed">
                Content ({document.content.length.toLocaleString()} characters)
              </Text>
            }
            labelPosition="center"
            style={{ borderColor: 'var(--warm-gray)' }}
          />

          {/* Document content */}
          {isMarkdown ? (
            <Box
              style={{
                fontSize: '15px',
                lineHeight: 1.7,
                color: 'var(--cream)',
              }}
              className="markdown-content"
            >
              <ReactMarkdown>{document.content}</ReactMarkdown>
            </Box>
          ) : (
            <Text
              size="sm"
              style={{
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-word',
                fontFamily: 'Fira Code, monospace',
                color: 'var(--cream)',
              }}
            >
              {document.content}
            </Text>
          )}
        </Box>
      </ScrollArea>

      <style>{`
        /* Markdown headings with Lumentor theme colors */
        .markdown-content h1 {
          font-family: 'Playfair Display', Georgia, serif;
          font-size: 2em;
          margin-top: 1.2em;
          margin-bottom: 0.6em;
          font-weight: 700;
          background: linear-gradient(135deg, var(--amber-light), var(--amber));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }
        .markdown-content h2 {
          font-family: 'Playfair Display', Georgia, serif;
          font-size: 1.6em;
          margin-top: 1em;
          margin-bottom: 0.5em;
          font-weight: 700;
          color: var(--amber);
        }
        .markdown-content h3 {
          font-family: 'Playfair Display', Georgia, serif;
          font-size: 1.3em;
          margin-top: 0.8em;
          margin-bottom: 0.4em;
          font-weight: 600;
          color: var(--amber-light);
        }
        .markdown-content h4 {
          font-weight: 600;
          color: var(--teal-light);
          margin-top: 0.6em;
          margin-bottom: 0.3em;
        }
        .markdown-content h5,
        .markdown-content h6 {
          font-weight: 600;
          color: var(--warm-gray);
          margin-top: 0.5em;
          margin-bottom: 0.25em;
        }

        /* Paragraph and text */
        .markdown-content p {
          margin-bottom: 1em;
          color: var(--cream);
        }

        /* Lists */
        .markdown-content ul,
        .markdown-content ol {
          margin-bottom: 1em;
          padding-left: 2em;
          color: var(--cream);
        }
        .markdown-content li {
          margin-bottom: 0.5em;
        }

        /* Inline code */
        .markdown-content code {
          background-color: var(--charcoal-lighter);
          color: var(--amber-light);
          padding: 2px 6px;
          border-radius: 3px;
          font-family: 'Fira Code', monospace;
          font-size: 0.9em;
          border: 1px solid rgba(245, 158, 11, 0.2);
        }

        /* Code blocks */
        .markdown-content pre {
          background-color: var(--charcoal-lighter);
          border: 1px solid var(--warm-gray);
          padding: 1em;
          border-radius: 6px;
          overflow-x: auto;
          margin-bottom: 1em;
        }
        .markdown-content pre code {
          background-color: transparent;
          border: none;
          padding: 0;
          color: var(--cream-dim);
        }

        /* Blockquotes */
        .markdown-content blockquote {
          border-left: 4px solid var(--teal);
          padding-left: 1em;
          margin-left: 0;
          margin-bottom: 1em;
          color: var(--cream-dim);
          font-style: italic;
        }

        /* Horizontal rule */
        .markdown-content hr {
          margin: 1.5em 0;
          border: none;
          border-top: 2px solid var(--warm-gray);
        }

        /* Links */
        .markdown-content a {
          color: var(--teal-light);
          text-decoration: underline;
        }
        .markdown-content a:hover {
          color: var(--amber);
        }

        /* Strong/bold */
        .markdown-content strong {
          color: var(--amber-light);
          font-weight: 600;
        }

        /* Emphasis/italic */
        .markdown-content em {
          color: var(--cream-dim);
          font-style: italic;
        }
      `}</style>
    </Modal>

    <LinkToCollectionModal
      key={`${document.id}-${document.collections?.join(',') || 'none'}`}
      opened={isLinkModalOpen}
      onClose={() => setIsLinkModalOpen(false)}
      onSuccess={handleLinkSuccess}
      documentId={document.id}
      documentTitle={document.filename}
      currentCollections={document.collections || []}
      availableCollections={availableCollections}
    />
    </>
  );
}
