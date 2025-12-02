import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Navbar } from '@/components/Navbar';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';
import { supabase } from '@/integrations/supabase/client';
import { toast } from 'sonner';

interface Video {
  id: string;
  title: string;
  description: string;
  video_url: string;
  created_at: string;
}

const Watch = () => {
  const { id } = useParams<{ id: string }>();
  const [video, setVideo] = useState<Video | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      fetchVideo(id);
    }
  }, [id]);

  const fetchVideo = async (videoId: string) => {
    try {
      const { data, error } = await supabase
        .from('videos')
        .select('*')
        .eq('id', videoId)
        .maybeSingle();

      if (error) throw error;
      
      if (!data) {
        toast.error('Video not found');
      } else {
        setVideo(data);
      }
    } catch (error: any) {
      toast.error('Failed to load video');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="flex justify-center items-center py-20">
          <div className="text-center">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent mx-auto mb-4" />
            <p className="text-muted-foreground">Loading video...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!video) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="container mx-auto px-4 py-8">
          <div className="text-center py-20">
            <p className="text-muted-foreground text-lg mb-4">Video not found</p>
            <Link to="/">
              <Button variant="outline" className="gap-2">
                <ArrowLeft className="w-4 h-4" />
                Back to Home
              </Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="container mx-auto px-4 py-8">
        <Link to="/">
          <Button variant="outline" className="mb-6 gap-2">
            <ArrowLeft className="w-4 h-4" />
            Back to Videos
          </Button>
        </Link>

        <div className="max-w-5xl mx-auto">
          <div className="aspect-video bg-black rounded-lg overflow-hidden mb-6 shadow-2xl">
            <video
              controls
              className="w-full h-full"
              src={video.video_url}
            >
              Your browser does not support the video tag.
            </video>
          </div>

          <div className="space-y-4">
            <h1 className="text-3xl font-bold">
              {video.title}
            </h1>
            
            {video.description && (
              <div className="bg-secondary rounded-lg p-4">
                <p className="text-foreground whitespace-pre-wrap">
                  {video.description}
                </p>
              </div>
            )}

            <div className="text-sm text-muted-foreground">
              Uploaded {new Date(video.created_at).toLocaleDateString()}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Watch;