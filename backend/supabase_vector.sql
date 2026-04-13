create extension if not exists vector;

create table if not exists public.event_embeddings (
    event_id integer primary key references public.events(id) on delete cascade,
    nation_id integer not null references public.nations(id) on delete cascade,
    turn_id integer not null references public.turns(id) on delete cascade,
    event_type varchar(50) not null,
    importance integer not null default 5,
    description text not null,
    event_metadata jsonb not null default '{}'::jsonb,
    embedding vector(384) not null,
    created_at timestamp without time zone not null default now()
);

create index if not exists event_embeddings_nation_id_idx on public.event_embeddings (nation_id);
create index if not exists event_embeddings_turn_id_idx on public.event_embeddings (turn_id);
create index if not exists event_embeddings_event_type_idx on public.event_embeddings (event_type);
create index if not exists event_embeddings_importance_idx on public.event_embeddings (importance);
create index if not exists event_embeddings_created_at_idx on public.event_embeddings (created_at desc);

create index if not exists event_embeddings_embedding_idx
on public.event_embeddings
using ivfflat (embedding vector_cosine_ops)
with (lists = 100);