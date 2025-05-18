import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import data from '../../Components/data.json';

const Appointment = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [service, setService] = useState(null);
  const [selectedOptions, setSelectedOptions] = useState([]);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });

    const timer = setTimeout(() => {
      // Find the service across all categories
      let foundService = null;
      for (const category of data.categories) {
        const s = category.services.find(s => s.id === id);
        if (s) {
          foundService = s;
          break;
        }
      }
      setService(foundService);
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, [id]);

  const handleOptionChange = (optionId) => {
    setSelectedOptions(prev => 
      prev.includes(optionId) 
        ? prev.filter(id => id !== optionId) 
        : [...prev, optionId]
    );
  };

  const calculateTotal = () => {
    if (!service) return 0;
    let total = parseFloat(service.price);
    service.appointment_options.forEach(option => {
      if (selectedOptions.includes(option.id)) {
        total += parseFloat(option.extra_cost);
      }
    });
    return total.toFixed(2);
  };

  const goBack = () => {
    navigate(-1);
  };

  return (
    <section className="bg-gray-50 min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Back Button */}
        <div className="mb-6">
          <button
            onClick={goBack}
            className="flex items-center text-[#e3a5b3] font-semibold hover:text-[#d69e91] transition-colors duration-200"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="w-6 h-6 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              strokeWidth="2"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
            Back
          </button>
        </div>

        {loading ? (
          <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-[#e3a5b3] animate-pulse">
            <div className="h-8 bg-gray-300 rounded w-3/4 mb-4"></div>
            <div className="h-6 bg-gray-200 rounded w-1/2 mb-6"></div>
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="flex items-center">
                  <div className="h-6 w-6 bg-gray-200 rounded mr-3"></div>
                  <div className="h-5 bg-gray-200 rounded w-1/3"></div>
                  <div className="h-5 bg-gray-200 rounded w-16 ml-auto"></div>
                </div>
              ))}
            </div>
            <div className="h-12 bg-gray-300 rounded-full w-48 mt-8 mx-auto"></div>
          </div>
        ) : service ? (
          <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-[#e3a5b3]">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">{service.title}</h1>
            <p className="text-xl text-[#e3a5b3] font-semibold mb-6">
              Base Price: £{service.price} • {service.duration}
            </p>
            
            <p className="text-gray-700 mb-8">{service.description}</p>
            
            {service.appointment_options?.length > 0 && (
              <>
                <h2 className="text-xl font-semibold text-gray-800 mb-4">Customization Options</h2>
                <div className="space-y-4 mb-8">
                  {service.appointment_options.map(option => (
                    <div key={option.id} className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50">
                      <div className="flex items-center">
                        <input
                          type="checkbox"
                          id={`option-${option.id}`}
                          checked={selectedOptions.includes(option.id)}
                          onChange={() => handleOptionChange(option.id)}
                          className="h-5 w-5 text-[#e3a5b3] rounded border-gray-300 focus:ring-[#e3a5b3]"
                        />
                        <label htmlFor={`option-${option.id}`} className="ml-3 text-gray-700">
                          {option.name}
                          {option.extra_duration && (
                            <span className="text-sm text-gray-500 ml-2">(+{option.extra_duration})</span>
                          )}
                        </label>
                      </div>
                      <span className="text-gray-900 font-medium">+£{option.extra_cost}</span>
                    </div>
                  ))}
                </div>
              </>
            )}

            <div className="border-t pt-6 mt-6">
              <div className="flex justify-between items-center mb-6">
                <span className="text-xl font-semibold">Total:</span>
                <span className="text-2xl font-bold text-[#e3a5b3]">£{calculateTotal()}</span>
              </div>
              
              <button
                className="w-full bg-[#e3a5b3] text-white font-medium py-3 rounded-full shadow-md hover:bg-[#d69e91] transition-colors duration-300"
                onClick={() => alert('Booking functionality would go here')}
              >
                Confirm Booking
              </button>
            </div>
          </div>
        ) : (
          <div className="text-center py-12">
            <h2 className="text-2xl font-semibold text-gray-800">Service not found</h2>
            <button
              onClick={goBack}
              className="mt-4 bg-[#e3a5b3] text-white px-6 py-2 rounded-full hover:bg-[#d69e91] transition-colors"
            >
              Back to Services
            </button>
          </div>
        )}
      </div>
    </section>
  );
};

export default Appointment;