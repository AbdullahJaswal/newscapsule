import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { News } from "@/types/News";
import ClientDateFormatter from "@/components/utils/client-date-formatter";
import { Clock, Images } from "lucide-react";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
} from "@/components/ui/carousel";
import Image from "next/image";

type Props = {
  article: News;
};

export default function NewsCard(props: Props) {
  return (
    <Card className="grid grid-cols-12 gap-2 hover:border-primary transition-colors duration-100">
      <Carousel className="col-span-3 w-full max-w-xs flex justify-center items-center">
        <CarouselContent>
          {props.article.newsDetails.map((detail) => {
            if (detail.thumbnail) {
              return (
                <CarouselItem key={`add-${detail.id}`}>
                  <Card className="border-0">
                    <CardContent className="flex aspect-square items-center justify-center p-0">
                      {detail.thumbnail ? (
                        <Image
                          alt="Product image"
                          className="aspect-square w-full rounded-l-md rounded-r-none object-cover"
                          height="300"
                          src={detail.thumbnail}
                          width="300"
                        />
                      ) : (
                        <Images className="w-80 h-80 text-muted-foreground" />
                      )}
                    </CardContent>
                  </Card>
                </CarouselItem>
              );
            }
          })}
        </CarouselContent>
      </Carousel>

      <div className="col-span-9">
        <CardHeader>
          <CardTitle className="text-xl">{props.article.titleText}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-xs text-muted-foreground flex flex-row gap-2">
            {props.article.newsDetails.map((detail) => {
              return (
                <div key={`ads-${detail.id}`}>
                  • <span>{detail.summary}</span>
                </div>
              );
            })}
          </div>
        </CardContent>

        <CardFooter className="mt-32 flex justify-end">
          <span className="w-4 h-4 flex items-center text-primary mr-2">
            <Clock />
          </span>
          <span className="text-xs text-muted-foreground">
            <ClientDateFormatter date={props.article.createdAt} />
          </span>
        </CardFooter>
      </div>
    </Card>
  );
}
