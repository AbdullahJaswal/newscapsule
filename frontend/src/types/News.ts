export type News = {
  id: number;
  title: string;
  titleText: string;
  slug: string;
  createdAt: string;
  updatedAt: string;
  newsDetails: NewsDetail[];
};

export type NewsDetail = {
  id: number;
  summary: string;
  description: string | null;
  thumbnail: string | null;
  image: string | null;
  timestamp: string;
  url: string;
  createdAt: string;
  updatedAt: string;
};
