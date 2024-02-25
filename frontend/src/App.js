import React from 'react';
import SequenceForm from './components/SequenceForm';
import JobsTable from './components/JobsTable';


/**
 * Shows a form to input a sequence and a table to display the jobs
 * @return {component} App
 */
function App() {
  return (
    <div>
      <SequenceForm />
      <JobsTable />
    </div>

  );
}

export default App;
