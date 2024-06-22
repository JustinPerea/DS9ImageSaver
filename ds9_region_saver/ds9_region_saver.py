import subprocess
import time
import os
import math

class DS9RegionSaver:
    def __init__(self, fits_files, colors, region_files, output_dir, scaling_params, source_file=None, name_file=None, padding=0.1):
        self.fits_files = fits_files
        self.colors = colors
        self.region_files = region_files
        self.output_dir = output_dir
        self.scaling_params = scaling_params  # List of dicts with scaling params for each FITS file
        self.source_file = source_file
        self.name_file = name_file
        self.padding = padding
        self.source_names = self._load_source_names() if name_file else {}

    def _run_xpaset_command(self, command):
        full_command = f"xpaset -p ds9 {command}"
        print(f"Running command: {full_command}")
        try:
            result = subprocess.run(full_command.split(), capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
            result.check_returncode()
        except subprocess.CalledProcessError as e:
            if "couldn't open" in e.stderr:
                print(f"Ignoring non-critical error: {e}")
            else:
                print(f"Error running command: {e}")
                print(e.output)
        time.sleep(1)  # Add a delay to ensure DS9 processes the command

    def _load_sources(self):
        sources = []
        with open(self.source_file, 'r') as file:
            lines = file.readlines()

        for line in lines:
            parts = line.strip().split()
            if len(parts) < 3:
                raise ValueError(f"Incorrect format in source file line: {line}")
            ra = parts[0]
            dec = parts[1]
            radius_arcsec = float(parts[2])
            sources.append((ra, dec, radius_arcsec))

        return sources

    def _load_source_names(self):
        source_names = {}
        with open(self.name_file, 'r') as file:
            lines = file.readlines()

        for line in lines:
            parts = line.strip().split()
            if len(parts) < 3:
                raise ValueError(f"Incorrect format in name file line: {line}")
            name = parts[0]
            ra = parts[1]
            dec = parts[2]
            source_names[(ra, dec)] = name  # (RA, Dec) -> Name

        return source_names

    def _calculate_zoom_level(self, field_of_view_deg):
        # Assume a base field of view for the full image
        base_field_of_view_deg = 0.1  # Adjust this based on your image's field of view
        zoom_factor = base_field_of_view_deg / field_of_view_deg if field_of_view_deg > 0 else 1
        return zoom_factor

    def save_images(self):
        # Ensure the output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        # Check permissions
        if not os.access(self.output_dir, os.W_OK):
            raise PermissionError(f"Cannot write to the directory: {self.output_dir}")

        # Start DS9 and load the FITS files as an RGB composite
        ds9_command = ['ds9', '-rgb']
        for fits_file, color, params in zip(self.fits_files, self.colors, self.scaling_params):
            ds9_command.extend([f'-{color}', fits_file])
            ds9_command.extend(['-scale', params['scaling']])
            ds9_command.extend(['-scale', 'limits', str(params['scale_min']), str(params['scale_max'])])
            ds9_command.extend(['-cmap', 'value', str(params['contrast']), str(params['bias'])])
        for region_file in self.region_files:
            ds9_command.extend(['-regions', region_file])
        ds9_process = subprocess.Popen(ds9_command)
        time.sleep(5)  # Wait a bit to ensure DS9 loads the files

        # Load the sources
        sources = self._load_sources()

        for i, (ra, dec, radius_arcsec) in enumerate(sources):
            # Convert radius from arcseconds to degrees
            radius_deg = radius_arcsec / 3600

            # Calculate the field of view required and zoom level
            field_of_view_deg = radius_deg * 20 * (1 + self.padding)
            zoom_level = self._calculate_zoom_level(field_of_view_deg)
            print(f"Source {i+1}: RA={ra}, Dec={dec}, Radius (deg)={radius_deg}, Field of View (deg)={field_of_view_deg}, Zoom Level={zoom_level}")

            # Set the zoom level
            self._run_xpaset_command(f"zoom to {zoom_level}")

            # Pan to the region
            self._run_xpaset_command(f"pan to {ra} {dec} wcs fk5")

            # Add label to the image
            source_name = self.source_names.get((ra, dec), f"Source_{i+1}")
            self._run_xpaset_command(f"regions command '{{text {ra} {dec} # text=\"{source_name}\" color=white}}'")

            # Save the image
            output_image = os.path.join(self.output_dir, f"{source_name}_region_{i+1}.png")
            try:
                self._run_xpaset_command(f"saveimage png {output_image}")
            except subprocess.CalledProcessError as e:
                if "couldn't open" in e.stderr:
                    print(f"Ignoring non-critical error: {e}")
                else:
                    print(f"Error saving image: {output_image}")
                    print(e)

        # Close DS9
        self._run_xpaset_command("exit")
        ds9_process.wait()  # Ensure DS9 process is terminated