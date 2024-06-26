import { CustomSlider } from "@/components/slider";
import { TourismCard } from "@/components/tourism-card";
import { PostCard } from "@/components/post-card";

export default function Home() {
  return (
    <div className="flex flex-col gap-8 py-8">
      <h1 className="uppercase text-custom-main text-7xl font-bold text-center">
        Внутренний туризм
      </h1>

      <CustomSlider>
        {[0, 1, 2, 3, 4, 5].map((item) => (
          <div key={item}>
            <TourismCard
              className="max-w-80"
              raiting="4,9"
              name="Внедрение современных методик способствует повышению качества"
            />
          </div>
        ))}
      </CustomSlider>

      <div className="">
        <h2 className="uppercase text-4xl font-semibold px-4">
          Популярные статьи
        </h2>
        <CustomSlider buttonsWithBg={false} slidesToShow={3}>
          {[0, 1, 2, 3, 4, 5].map((item) => (
            <div key={item}>
              <PostCard />
            </div>
          ))}
        </CustomSlider>
      </div>
    </div>
  );
}
