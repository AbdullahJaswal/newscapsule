import { News } from "@/types/News";
import NewsCard from "@/components/news-card";

async function getNews() {
  const res = await fetch(`${process.env.NEXT_PRIVATE_API_URL}/news/`);
  // The return value is *not* serialized
  // You can return Date, Map, Set, etc.

  if (!res.ok) {
    // This will activate the closest `error.js` Error Boundary
    throw new Error("Failed to fetch data");
  }

  return res.json();
}

export default async function NewsSection() {
  const news: News[] = await getNews();

  return (
    <div className="flex flex-col gap-4">
      {news.map((article) => (
        <NewsCard key={`a-${article.id}`} article={article} />
      ))}
    </div>
  );
}
