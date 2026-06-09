import { AddPlateForm } from '@/features/plates/components/add-plate-form';
import { PlatesTable } from '@/features/plates/components/plates-table';

const PlatesPage = () => (
  <div className="page page-grid">
    <PlatesTable />
    <AddPlateForm />
  </div>
);

export default PlatesPage;
