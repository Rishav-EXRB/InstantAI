import React, { useRef } from "react";
import { UserProfile } from "../types";
import { Camera } from "lucide-react";

export default function Profile({
  user,
  onUserUpdate,
  onLogout,
}: {
  user: UserProfile;
  onUserUpdate: (u: UserProfile) => void;
  onLogout: () => void;
}) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageUpload = (file: File) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      onUserUpdate({
        ...user,
        avatar: reader.result as string,
      });
    };
    reader.readAsDataURL(file);
  };

  console.log("Profile render, avatar =", user.avatar);


  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-1">Profile</h1>
      <p className="text-slate-500 mb-8">
        Account information and authentication details
      </p>

      <div className="bg-white rounded-3xl border border-slate-200 p-8 space-y-8">
        {/* Avatar Section */}
        <div className="flex items-center gap-6">
          <div
            onClick={() => fileInputRef.current?.click()}
            className="relative cursor-pointer group"
          >
            {user.avatar ? (
              <img
                src={user.avatar}
                alt="Profile"
                className="w-24 h-24 rounded-full object-cover border"
              />
            ) : (
              <div className="w-24 h-24 rounded-full bg-gradient-to-br from-blue-600 to-indigo-600 text-white flex items-center justify-center text-3xl font-bold">
                {user.name
                  .split(" ")
                  .map((n) => n[0])
                  .join("")}
              </div>
            )}

            {/* Hover Overlay */}
            <div className="absolute inset-0 bg-black/40 rounded-full opacity-0 group-hover:opacity-100 flex items-center justify-center transition-all">
              <Camera className="text-white" />
            </div>
          </div>

          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) =>
              e.target.files && handleImageUpload(e.target.files[0])
            }
          />

          <div>
            <h2 className="text-xl font-bold">{user.name}</h2>
            <p className="text-slate-500">{user.designation}</p>
            <span className="inline-block mt-2 text-xs font-bold uppercase tracking-widest text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
              {user.authLevel}
            </span>
          </div>
        </div>

        {/* Details */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Field label="Full Name" value={user.name} />
          <Field label="Designation" value={user.designation} />
          <Field label="Authentication Level" value={user.authLevel} />
          <Field label="Account Status" value="Active" />
        </div>

        {/* Logout */}
        <div className="pt-6 border-t border-slate-200">
          <button
            onClick={onLogout}
            className="px-6 py-2 rounded-xl bg-rose-600 text-white font-bold hover:bg-rose-700 transition-all"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs uppercase tracking-widest text-slate-400 mb-1">
        {label}
      </p>
      <p className="font-semibold">{value}</p>
    </div>
  );
}
