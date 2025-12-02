import { Link } from 'react-router-dom';
import { Play } from 'lucide-react';
import { Card } from '@/components/ui/card';

interface VideoCardProps {
  id: string;
  title: string;
  description: string;
  thumbnailUrl?: string;
}

export const VideoCard = ({ id, title, description, thumbnailUrl }: VideoCardProps) => {
  return (
    <Link to={`/watch/${id}`}>
      <Card className="group overflow-hidden border-border/50 hover:border-primary/50 transition-all duration-300 hover:shadow-glow">
        <div className="relative aspect-video bg-secondary overflow-hidden">
          {thumbnailUrl ? (
            <img 
              src={thumbnailUrl} 
              alt={title}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <Play className="w-16 h-16 text-muted-foreground group-hover:text-primary transition-colors" />
            </div>
          )}
          <div className="absolute inset-0 bg-gradient-to-t from-background/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
            <div className="bg-primary/90 backdrop-blur-sm rounded-full p-4">
              <Play className="w-8 h-8 text-primary-foreground fill-primary-foreground" />
            </div>
          </div>
        </div>
        <div className="p-4">
          <h3 className="font-semibold text-lg mb-1 line-clamp-2 text-foreground group-hover:text-foreground/80 transition-colors">
            {title}
          </h3>
          {description && (
            <p className="text-sm text-muted-foreground line-clamp-2">
              {description}
            </p>
          )}
        </div>
      </Card>
    </Link>
  );
};