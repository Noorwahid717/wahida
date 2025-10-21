import type { Meta, StoryObj } from '@storybook/react';
import { QuizCard } from './quiz-card';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

const meta = {
  title: 'Components/QuizCard',
  component: QuizCard,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Interactive quiz card component for educational questions.',
      },
    },
  },
  decorators: [
    (Story: React.ComponentType) => (
      <QueryClientProvider client={queryClient}>
        <div className="max-w-md">
          <Story />
        </div>
      </QueryClientProvider>
    ),
  ],
  tags: ['autodocs'],
} satisfies Meta<typeof QuizCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    questionId: 'q1',
    prompt: 'Apa hasil dari 2 + 2?',
    choices: ['3', '4', '5', '6'],
  },
};

export const MultipleChoice: Story = {
  args: {
    questionId: 'q2',
    prompt: 'Manakah yang merupakan bahasa pemrograman?',
    choices: ['HTML', 'Python', 'CSS', 'SQL'],
  },
};

export const CorrectAnswer: Story = {
  args: {
    questionId: 'q3',
    prompt: 'Berapa nilai π (pi) hingga 2 desimal?',
    choices: ['3.14', '3.15', '3.16', '3.17'],
  },
};

export const LongQuestion: Story = {
  args: {
    questionId: 'q4',
    prompt: 'Dalam konteks kecerdasan buatan, apa yang dimaksud dengan "machine learning"?',
    choices: [
      'Komputer yang bisa berbicara seperti manusia',
      'Algoritma yang belajar dari data tanpa diprogram secara eksplisit',
      'Robot yang bisa berjalan sendiri',
      'Program yang bisa menerjemahkan bahasa',
    ],
  },
};