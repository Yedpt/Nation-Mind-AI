export interface NationCardProps {
  name: string;
  resources: number;
  power: number;
}

export default function NationCard({ name, resources, power }: NationCardProps) {
  return (
    <div className="border p-4 rounded-lg shadow-md">
      <h3 className="text-xl font-bold">{name}</h3>
      <p>Recursos: {resources}</p>
      <p>Poder: {power}</p>
    </div>
  );
}